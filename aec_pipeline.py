"""
End‑to‑end AEC pipeline.

This module exposes the :class:`AECPipeline` class, which ties together the
retrieval, planning, coding and verification agents into a coherent workflow.
Given an input text and an event schema the pipeline can use heuristic or
LLM-based planning, and can optionally generate multiple event objects for a
single text when the coding stage is LLM-assisted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    from .event_schema import EventSchema, EventObject
    from .retrieval_agent import RetrievalAgent
    from .planning_agent import PlanningAgent, Hypothesis
    from .coding_agent import CodingAgent
    from .verification_agent import VerificationAgent, VerificationError
    from .ontology import OntologyManager
except ImportError:
    from event_schema import EventSchema, EventObject
    from retrieval_agent import RetrievalAgent
    from planning_agent import PlanningAgent, Hypothesis
    from coding_agent import CodingAgent
    from verification_agent import VerificationAgent, VerificationError
    from ontology import OntologyManager


def _schema_to_definition_text(schema: EventSchema) -> str:
    event_defs = "from dataclasses import dataclass\nfrom typing import List\n\n@dataclass\n"
    event_defs += f"class {schema.event_type}:\n"
    event_defs += "    mention: str\n"
    for role in schema.roles.keys():
        event_defs += f"    {role}: List\n"
    return event_defs


@dataclass
class AECPipeline:
    """High-level orchestrator for the AEC multi-agent pipeline."""

    retrieval_agent: RetrievalAgent = field(default_factory=RetrievalAgent)
    planning_agent: PlanningAgent = field(default_factory=PlanningAgent)
    coding_agent: CodingAgent = field(default_factory=CodingAgent)
    verification_agent: VerificationAgent = field(default_factory=VerificationAgent)
    ontology_manager: Optional["OntologyManager"] = None  # type: ignore[name-defined]
    max_hypotheses: int = 3
    max_patches: int = 2
    use_llm_plan: bool = False
    use_llm_coding: bool = False
    planning_profile: str = "generic"
    trigger_adapter: str = "none"
    output_adapter: str = "none"
    repair_mode: str = "full"
    planning_backend: str = "aec"
    last_run_trace: List[Dict[str, Any]] = field(default_factory=list, init=False)
    last_run_summary: Dict[str, Any] = field(default_factory=dict, init=False)

    def _annotate_repair_outcomes(self, trace_steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for idx, step in enumerate(trace_steps):
            if step.get("stage") != "repair":
                continue
            prior_info = step.get("error_info") if isinstance(step.get("error_info"), dict) else {}
            prior_category = prior_info.get("category")
            next_verify = next(
                (
                    candidate
                    for candidate in trace_steps[idx + 1 :]
                    if candidate.get("stage") == "verify"
                ),
                None,
            )
            if next_verify is None:
                step["repair_outcome"] = {
                    "status": "unknown",
                    "from_category": prior_category,
                    "to_category": None,
                    "reason": "no subsequent verification step recorded",
                }
                continue
            if next_verify.get("status") == "passed":
                step["repair_outcome"] = {
                    "status": "resolved",
                    "from_category": prior_category,
                    "to_category": "passed",
                    "reason": "the next verification step passed after this repair",
                }
                continue
            next_info = next_verify.get("error_info") if isinstance(next_verify.get("error_info"), dict) else {}
            next_category = next_info.get("category")
            if next_category == prior_category:
                status = "unchanged"
                reason = "the same verifier category remained after repair"
            else:
                status = "shifted"
                reason = "repair changed the verifier failure category"
            step["repair_outcome"] = {
                "status": status,
                "from_category": prior_category,
                "to_category": next_category,
                "reason": reason,
            }
        return trace_steps

    def _increment_counter(self, bucket: Dict[str, int], key: str | None) -> None:
        normalized = key or "unknown"
        bucket[normalized] = bucket.get(normalized, 0) + 1

    def _build_run_summary(self, validated_events: List[EventObject]) -> Dict[str, Any]:
        summary: Dict[str, Any] = {
            "hypothesis_count": len(self.last_run_trace),
            "validated_event_count": len(validated_events),
            "verified_pass_count": 0,
            "verified_fail_count": 0,
            "repair_attempt_count": 0,
            "repair_changed_count": 0,
            "verifier_categories": {},
            "repair_routes": {},
            "repair_outcomes": {},
        }
        category_counts = summary["verifier_categories"]
        route_counts = summary["repair_routes"]
        outcome_counts = summary["repair_outcomes"]
        for hypothesis_trace in self.last_run_trace:
            for attempt in hypothesis_trace.get("attempts", []):
                repair_info = attempt.get("hypothesis_repair")
                if isinstance(repair_info, dict):
                    self._increment_counter(route_counts, repair_info.get("route"))
                for verification in attempt.get("verification", []):
                    for step in verification.get("trace", []):
                        if step.get("stage") == "verify":
                            status = step.get("status")
                            if status == "passed":
                                summary["verified_pass_count"] += 1
                            elif status == "failed":
                                summary["verified_fail_count"] += 1
                                error_info = step.get("error_info") if isinstance(step.get("error_info"), dict) else {}
                                self._increment_counter(category_counts, error_info.get("category"))
                        elif step.get("stage") == "repair":
                            summary["repair_attempt_count"] += 1
                            self._increment_counter(route_counts, step.get("route"))
                            self._increment_counter(route_counts, step.get("route"))
                            if step.get("changed"):
                                summary["repair_changed_count"] += 1
                            outcome = step.get("repair_outcome") if isinstance(step.get("repair_outcome"), dict) else {}
                            self._increment_counter(outcome_counts, outcome.get("status"))
        return summary

    def _drop_arguments_for_ti_first(
        self,
        event_obj: EventObject,
        schema: EventSchema,
        text: str,
        error_info: Dict[str, Any] | None,
    ) -> tuple[Optional[EventObject], Dict[str, Any] | None]:
        if self.planning_backend != "dicore" or self.planning_profile != "genia":
            return None, None
        if not isinstance(error_info, dict):
            return None, None
        category = error_info.get("category")
        if category not in {"argument_not_locally_bound", "argument_crosses_clause_boundary"}:
            return None, None
        if not any(event_obj.arguments.values()):
            return None, None
        fallback_event = EventObject(
            event_type=event_obj.event_type,
            trigger=event_obj.trigger,
            arguments={role: [] for role in schema.roles},
        )
        try:
            self.verification_agent.verify(fallback_event, schema, text)
        except VerificationError:
            return None, None
        return fallback_event, {
            "stage": "ti_first_argument_drop",
            "status": "passed",
            "trigger": fallback_event.trigger,
            "arguments": fallback_event.arguments,
            "reason": "kept a verified trigger by dropping arguments after argument-boundary verification failure",
        }

    def _drop_failed_argument_for_ti(
        self,
        event_obj: EventObject,
        schema: EventSchema,
        text: str,
        error_info: Dict[str, Any] | None,
    ) -> tuple[Optional[EventObject], Dict[str, Any] | None]:
        if self.planning_backend != "dicore" or self.planning_profile != "genia":
            return None, None
        if not isinstance(error_info, dict):
            return None, None
        category = error_info.get("category")
        if category not in {"argument_not_locally_bound", "argument_crosses_clause_boundary"}:
            return None, None
        details = error_info.get("details") if isinstance(error_info.get("details"), dict) else {}
        role = details.get("role")
        if not isinstance(role, str) or role not in event_obj.arguments:
            return None, None
        fallback_args = {name: list(values) for name, values in event_obj.arguments.items()}
        if not fallback_args.get(role):
            return None, None
        fallback_args[role] = []
        fallback_event = EventObject(
            event_type=event_obj.event_type,
            trigger=event_obj.trigger,
            arguments=fallback_args,
        )
        try:
            self.verification_agent.verify(fallback_event, schema, text)
        except VerificationError:
            return None, None
        return fallback_event, {
            "stage": "ti_first_argument_drop",
            "status": "passed",
            "dropped_role": role,
            "trigger": fallback_event.trigger,
            "arguments": fallback_event.arguments,
            "reason": "kept a verified trigger by dropping an argument that violated local-boundary constraints",
        }

    def _verify_and_patch_event(
        self,
        event_obj: EventObject,
        schema: EventSchema,
        text: str,
        *,
        allow_repair: bool,
    ) -> tuple[Optional[EventObject], List[Dict[str, Any]], Dict[str, Any] | None]:
        max_rounds = max(1, self.coding_agent.max_repair_rounds + 1)
        candidate = event_obj
        trace_steps: List[Dict[str, Any]] = []
        last_error_payload: Dict[str, Any] | None = None
        for attempt_idx in range(max_rounds):
            try:
                self.verification_agent.verify(candidate, schema, text)
                trace_steps.append(
                    {
                        "stage": "verify",
                        "attempt": attempt_idx + 1,
                        "status": "passed",
                        "trigger": candidate.trigger,
                        "arguments": candidate.arguments,
                    }
                )
                return candidate, self._annotate_repair_outcomes(trace_steps), None
            except VerificationError as exc:
                error_payload = exc.to_dict()
                last_error_payload = error_payload
                trace_steps.append(
                    {
                        "stage": "verify",
                        "attempt": attempt_idx + 1,
                        "status": "failed",
                        "trigger": candidate.trigger,
                        "arguments": candidate.arguments,
                        "error": str(exc),
                        "error_info": error_payload,
                    }
                )
                if not allow_repair or attempt_idx >= max_rounds - 1:
                    fallback_event, fallback_step = self._drop_failed_argument_for_ti(
                        candidate,
                        schema,
                        text,
                        error_payload,
                    )
                    if fallback_event is not None:
                        if fallback_step is not None:
                            trace_steps.append(fallback_step)
                        return fallback_event, self._annotate_repair_outcomes(trace_steps), None
                    break
                error_category = error_payload.get("category")
                if error_category in {"trigger_not_in_text", "event_type_mismatch"}:
                    break
                if self.repair_mode == "light":
                    break
                repaired = self.coding_agent.repair_event_object(
                    event_obj=candidate,
                    schema=schema,
                    text=text,
                    verification_error=str(exc),
                    verification_info=error_payload,
                )
                trace_steps.append(
                    {
                        "stage": "repair",
                        "attempt": attempt_idx + 1,
                        "route": "argument",
                        "from_trigger": candidate.trigger,
                        "to_trigger": repaired.trigger,
                        "arguments": repaired.arguments,
                        "error": str(exc),
                        "error_info": error_payload,
                        "changed": repaired.arguments != candidate.arguments or repaired.trigger != candidate.trigger,
                    }
                )
                candidate = repaired
        return None, self._annotate_repair_outcomes(trace_steps), last_error_payload

    def run(
        self,
        text: str,
        schema: Optional[EventSchema] = None,
        *,
        dataset: Optional[str] = None,
        event_type: Optional[str] = None,
        use_llm_plan: Optional[bool] = None,
        use_llm_coding: Optional[bool] = None,
    ) -> Optional[EventObject]:
        """Execute the pipeline and return the first validated event, if any."""
        events = self.run_many(
            text=text,
            schema=schema,
            dataset=dataset,
            event_type=event_type,
            use_llm_plan=use_llm_plan,
            use_llm_coding=use_llm_coding,
        )
        return events[0] if events else None

    def run_many(
        self,
        text: str,
        schema: Optional[EventSchema] = None,
        *,
        dataset: Optional[str] = None,
        event_type: Optional[str] = None,
        use_llm_plan: Optional[bool] = None,
        use_llm_coding: Optional[bool] = None,
    ) -> List[EventObject]:
        """Execute the pipeline and return all validated events for the text."""
        if schema is None:
            if self.ontology_manager is None:
                raise ValueError(
                    "Ontology manager is not set; please provide a schema or configure an ontology manager."
                )
            if not dataset or not event_type:
                raise ValueError("dataset and event_type must be provided when schema is None")
            schema = self.ontology_manager.get_schema(dataset, event_type)
            if schema is None:
                raise ValueError(f"No schema found for event type '{event_type}' in dataset '{dataset}'")

        examples = self.retrieval_agent.retrieve(schema, k=self.max_hypotheses)
        self.last_run_trace = []
        self.last_run_summary = {}
        use_llm = self.use_llm_plan if use_llm_plan is None else use_llm_plan
        use_llm_coding_effective = self.use_llm_coding if use_llm_coding is None else use_llm_coding

        hypotheses: List[Hypothesis]
        if use_llm:
            if self.ontology_manager is None or self.planning_profile == "mapcoder":
                event_defs = _schema_to_definition_text(schema)
            else:
                if not dataset:
                    raise ValueError(
                        "use_llm_plan=True requires a dataset argument to build event definitions."
                    )
                event_defs = self.ontology_manager.build_definitions(dataset)
            llm_hyps = self.planning_agent.generate_hypotheses_with_llm(
                text=text,
                event_definitions=event_defs,
                max_candidates=self.max_hypotheses * 2,
                exemplars=examples,
                planning_profile=self.planning_profile,
                planning_backend=self.planning_backend,
                trigger_adapter=self.trigger_adapter,
            )
            if event_type:
                llm_hyps = [h for h in llm_hyps if h.event_type.lower() == event_type.lower()]
            hypotheses = llm_hyps[: self.max_hypotheses]
            planner_debug = getattr(self.planning_agent, "last_planner_debug", None)
            if isinstance(planner_debug, dict) and planner_debug:
                self.last_run_trace.append({"stage": "planner_debug", "data": planner_debug})
        else:
            hypotheses = self.planning_agent.generate_hypotheses(
                text=text,
                schema=schema,
                examples=examples,
                k=self.max_hypotheses,
            )

        validated_events: List[EventObject] = []
        seen_triggers: set[str] = set()
        for hypothesis in hypotheses:
            hypothesis_trace: Dict[str, Any] = {
                "trigger": hypothesis.trigger,
                "event_type": hypothesis.event_type,
                "confidence": hypothesis.confidence,
                "rationale": hypothesis.rationale,
                "attempts": [],
            }
            current_hypothesis = hypothesis
            for patch_attempt in range(1, self.max_patches + 1):
                event_objs = self.coding_agent.generate_event_objects(
                    hypothesis=current_hypothesis,
                    schema=schema,
                    text=text,
                    use_llm_coding=use_llm_coding_effective,
                )
                attempt_trace: Dict[str, Any] = {
                    "patch_attempt": patch_attempt,
                    "generated_events": [
                        {
                            "trigger": event_obj.trigger,
                            "arguments": event_obj.arguments,
                        }
                        for event_obj in event_objs
                    ],
                    "verification": [],
                }
                any_success = False
                last_verification_error: str | None = None
                last_verification_info: Dict[str, Any] | None = None
                for event_obj in event_objs:
                    validated, trace_steps, terminal_error_info = self._verify_and_patch_event(
                        event_obj,
                        schema,
                        text,
                        allow_repair=True,
                    )
                    attempt_trace["verification"].append(
                        {
                            "initial_trigger": event_obj.trigger,
                            "trace": trace_steps,
                            "validated_trigger": validated.trigger if validated is not None else None,
                        }
                    )
                    if validated is not None:
                        output_event = self.coding_agent.normalize_genia_arguments_for_output(validated, text)
                        if "theme" in output_event.arguments and not output_event.arguments["theme"]:
                            refilled = self.coding_agent._apply_genia_theme_refill(
                                trigger=output_event.trigger,
                                event_type=output_event.event_type,
                                arguments=output_event.arguments,
                                role_names=list(schema.roles.keys()),
                                text=text,
                            )
                            if refilled.get("theme"):
                                output_event = EventObject(
                                    event_type=output_event.event_type,
                                    trigger=output_event.trigger,
                                    arguments={**output_event.arguments, "theme": refilled["theme"]},
                                )
                        if output_event.trigger not in seen_triggers:
                            validated_events.append(output_event)
                            seen_triggers.add(output_event.trigger)
                        any_success = True
                    elif trace_steps:
                        failed_steps = [
                            step for step in trace_steps if step.get("stage") == "verify" and step.get("status") == "failed"
                        ]
                        if failed_steps:
                            last_verification_error = failed_steps[-1].get("error")
                            raw_info = failed_steps[-1].get("error_info")
                            last_verification_info = raw_info if isinstance(raw_info, dict) else terminal_error_info
                hypothesis_trace["attempts"].append(attempt_trace)
                if any_success:
                    break
                if use_llm_coding_effective and last_verification_error and last_verification_info:
                    category = last_verification_info.get("category")
                    should_route_to_trigger = category in {"trigger_not_in_text", "event_type_mismatch"}
                    allow_hypothesis_repair = self.repair_mode != "none"
                    decision_basis = {
                        "category": category,
                        "details": last_verification_info.get("details", {}),
                        "policy": (
                            "route_to_trigger_repair"
                            if should_route_to_trigger
                            else "keep_trigger_and_prefer_argument_repair"
                        ),
                        "reason": (
                            "verifier category indicates the trigger or event-type alignment is wrong"
                            if should_route_to_trigger
                            else "verifier category indicates argument-level repair is the preferred first action"
                        ),
                    }
                    if should_route_to_trigger and allow_hypothesis_repair:
                        repaired_hypothesis = self.coding_agent.repair_trigger_hypothesis(
                            current_hypothesis,
                            text,
                            last_verification_error,
                            last_verification_info,
                        )
                        attempt_trace["hypothesis_repair"] = {
                            "from_trigger": current_hypothesis.trigger,
                            "to_trigger": repaired_hypothesis.trigger,
                            "error": last_verification_error,
                            "error_info": last_verification_info,
                            "route": "trigger",
                            "decision_basis": decision_basis,
                        }
                        current_hypothesis = repaired_hypothesis
                    else:
                        attempt_trace["hypothesis_repair"] = {
                            "from_trigger": current_hypothesis.trigger,
                            "to_trigger": current_hypothesis.trigger,
                            "error": last_verification_error,
                            "error_info": last_verification_info,
                            "route": "argument",
                            "decision_basis": decision_basis,
                        }
                        if not allow_hypothesis_repair:
                            break
            self.last_run_trace.append(hypothesis_trace)
        self.last_run_summary = self._build_run_summary(validated_events)
        return validated_events
