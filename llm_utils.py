"""
Utility functions for interacting with language models.

This module centralises calls to chat-style LLM services. By default it
supports OpenAI-hosted models such as ``gpt-4o`` and any OpenAI-compatible
endpoint exposed by local or self-hosted servers (for example vLLM, SGLang,
LM Studio, or Ollama-compatible proxies).

The active model/backend can be configured either via function arguments or
via environment variables:

- ``AEC_LLM_MODEL`` / ``OPENAI_MODEL``
- ``AEC_LLM_BASE_URL`` / ``OPENAI_BASE_URL``
- ``AEC_LLM_API_KEY`` / ``OPENAI_API_KEY``

If no base URL is provided, the official OpenAI endpoint is used.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore[assignment]

DEFAULT_MODEL = "gpt-4o"
DEFAULT_LOCAL_API_KEY = "EMPTY"
DEBUG_DIR_ENV = "AEC_LLM_DEBUG_DIR"
LOCAL_CONTEXT_WINDOW = 220

MODEL_ALIASES: dict[str, dict[str, str | None]] = {
    "llama3-8b": {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "base_url": None,
    },
    "llama3-70b": {
        "model": "meta-llama/Meta-Llama-3-70B-Instruct",
        "base_url": None,
    },
    "gpt3.5-turbo": {
        "model": "gpt-3.5-turbo",
        "base_url": "https://api.openai.com/v1",
    },
    "gpt4o": {
        "model": "gpt-4o",
        "base_url": "https://api.openai.com/v1",
    },
}

GENIA_EVENT_GUIDANCE: dict[str, str] = {
    "Positive_regulation": (
        "Definition: a positive regulation event where some factor increases, activates, induces, enhances, promotes, or stimulates another biological process or entity. "
        "Typical trigger forms include activate, activated, activation, induce, induced, induction, enhance, enhanced, stimulates, increased, increase, overexpression, and promote. "
        "Trigger rule: choose the smallest eventive word or phrase that directly expresses the positive regulatory change, not the affected participant."
    ),
    "Negative_regulation": (
        "Definition: a negative regulation event where some factor suppresses, inhibits, represses, blocks, reduces, decreases, dampens, abolishes, or down-regulates another biological process or entity. "
        "Typical trigger forms include inhibit, inhibited, inhibition, repress, repressed, suppress, suppressed, block, blocked, reduce, reduced, decrease, down-regulate, and abrogate. "
        "Trigger rule: choose the eventive expression of negative control itself, not the downstream target or assay outcome."
    ),
    "Binding": (
        "Definition: a binding or physical association event between molecules or molecular participants. "
        "Typical trigger forms include bind, binds, binding, interact, interacts, interaction, associate, associates, complex, complex formation, recruit, recruitment, and immunoprecipitated when they denote molecular association. "
        "Trigger rule: choose the association expression itself, not discourse words, section titles, or participant names."
    ),
    "Gene_expression": (
        "Definition: an event where a gene or protein is expressed or its expression is reported as an event mention. "
        "Typical trigger forms include expression, expressed, production, produced, synthesis, synthesized, and overexpressed when the wording denotes an expression event. "
        "Trigger rule: choose the expression event word, not the gene/protein name alone."
    ),
    "Transcription": (
        "Definition: a transcription event involving transcription, transcript generation, or mRNA production. "
        "Typical trigger forms include transcription, transcribed, transcript, transactivation when it truly denotes transcriptional activity, and mRNA expression when used as the event mention. "
        "Trigger rule: prefer the transcription-specific expression over broader regulation words when both appear nearby."
    ),
    "Localization": (
        "Definition: an event describing movement to a location, localization state, translocation, or recruitment to a site or compartment. "
        "Typical trigger forms include localize, localized, localization, translocation, recruit, recruitment, targeted, imported, exported, and moved when they denote spatial placement. "
        "Trigger rule: choose the movement or placement expression itself, not the location argument."
    ),
    "Protein_modification": (
        "Definition: a protein modification event describing that a protein becomes modified. "
        "Typical trigger forms include modification, modified, processing, cleavage, ubiquitination, methylation, and acetylation when they denote the modification event. "
        "Trigger rule: choose the modification expression itself, not the modified protein."
    ),
    "Phosphorylation": (
        "Definition: a phosphorylation event describing phosphorylation or phospho-status change. "
        "Typical trigger forms include phosphorylation, phosphorylated, phospho-, hyperphosphorylation, and dephosphorylation only when the target schema actually matches the event type. "
        "Trigger rule: choose the phosphorylation expression itself, not the residue or substrate alone."
    ),
}


def _get_event_specific_guidance(event_type: str, planning_profile: str) -> str:
    if planning_profile != "genia":
        return ""
    return GENIA_EVENT_GUIDANCE.get(event_type, "")


def _normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def _build_local_context(text: str, trigger: str, window: int = LOCAL_CONTEXT_WINDOW) -> str:
    normalized_text = _normalize_whitespace(text)
    normalized_trigger = _normalize_whitespace(trigger)
    if not normalized_text:
        return ""
    if not normalized_trigger:
        return normalized_text[: window * 2]
    trigger_idx = normalized_text.lower().find(normalized_trigger.lower())
    if trigger_idx == -1:
        return normalized_text[: window * 2]
    start = max(0, trigger_idx - window)
    end = min(len(normalized_text), trigger_idx + len(normalized_trigger) + window)
    return normalized_text[start:end]


def _build_trigger_sentence(text: str, trigger: str) -> str:
    normalized_text = _normalize_whitespace(text)
    normalized_trigger = _normalize_whitespace(trigger)
    if not normalized_text:
        return ""
    if not normalized_trigger:
        return normalized_text
    trigger_idx = normalized_text.lower().find(normalized_trigger.lower())
    if trigger_idx == -1:
        return normalized_text
    left_candidates = [normalized_text.rfind(marker, 0, trigger_idx) for marker in ".!?;"]
    left = max(left_candidates)
    right_candidates = [normalized_text.find(marker, trigger_idx) for marker in ".!?;"]
    right_candidates = [candidate for candidate in right_candidates if candidate != -1]
    right = min(right_candidates) if right_candidates else len(normalized_text)
    return normalized_text[left + 1:right].strip()


def resolve_llm_config(
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> tuple[str, str | None, str | None]:
    """Resolve model/backend configuration from args and environment."""
    raw_model = model or os.getenv("AEC_LLM_MODEL") or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    alias_config = MODEL_ALIASES.get(raw_model.lower())
    resolved_model = str(alias_config.get("model")) if alias_config else raw_model
    resolved_base_url = base_url or os.getenv("AEC_LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
    if not resolved_base_url and alias_config:
        alias_base_url = alias_config.get("base_url")
        resolved_base_url = str(alias_base_url) if alias_base_url else None
    resolved_api_key = api_key or os.getenv("AEC_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if resolved_base_url and not resolved_api_key:
        resolved_api_key = DEFAULT_LOCAL_API_KEY
    return resolved_model, resolved_base_url, resolved_api_key


def _debug_log_llm_reply(tag: str, reply: str) -> None:
    debug_dir = os.getenv(DEBUG_DIR_ENV)
    if not debug_dir:
        return
    path = Path(debug_dir)
    path.mkdir(parents=True, exist_ok=True)
    existing = sorted(path.glob(f"{tag}_*.txt"))
    next_idx = len(existing) + 1
    (path / f"{tag}_{next_idx:04d}.txt").write_text(reply, encoding="utf-8")


def _extract_json_fragment(reply: str) -> str:
    reply = reply.strip()
    if not reply:
        return reply
    fenced_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", reply)
    if fenced_match:
        return fenced_match.group(1).strip()

    candidates: List[str] = []
    for opener, closer in (("[", "]"), ("{", "}")):
        start = reply.find(opener)
        end = reply.rfind(closer)
        if start != -1 and end != -1 and end > start:
            candidates.append(reply[start : end + 1].strip())
    if candidates:
        candidates.sort(key=len, reverse=True)
        return candidates[0]
    return reply


def _load_json_reply(reply: str) -> Any | None:
    for candidate in (reply.strip(), _extract_json_fragment(reply)):
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except Exception:
            continue
    return None


def call_llm(
    messages: List[Dict[str, str]],
    model: str | None = None,
    *,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float = 0.0,
    request_tag: str = "llm",
    max_tokens: int | None = None,
) -> str:
    """Call a chat model and return the assistant text reply."""
    if OpenAI is None:
        raise RuntimeError(
            "openai package is not installed; please install it to use LLM features."
        )

    resolved_model, resolved_base_url, resolved_api_key = resolve_llm_config(
        model=model,
        base_url=base_url,
        api_key=api_key,
    )
    if not resolved_api_key:
        raise RuntimeError(
            "No API key configured. Set OPENAI_API_KEY/AEC_LLM_API_KEY, or provide "
            "an OpenAI-compatible base URL so a local server can be used."
        )

    timeout_seconds = float(os.getenv("AEC_LLM_TIMEOUT", "180"))
    retries = max(0, int(os.getenv("AEC_LLM_RETRIES", "1")))
    resolved_max_tokens = max_tokens if max_tokens is not None else int(os.getenv("AEC_LLM_MAX_TOKENS", "768"))
    resolved_top_p = float(os.getenv("AEC_LLM_TOP_P", "1.0"))
    seed_env = os.getenv("AEC_LLM_SEED")
    resolved_seed = int(seed_env) if seed_env not in {None, ""} else None
    verbose = os.getenv("AEC_LLM_VERBOSE", "1").lower() not in {"0", "false", "no"}
    fail_soft = os.getenv("AEC_LLM_FAIL_SOFT", "1").lower() not in {"0", "false", "no"}

    client_kwargs: Dict[str, str] = {"api_key": resolved_api_key}
    if resolved_base_url:
        client_kwargs["base_url"] = resolved_base_url
    client = OpenAI(**client_kwargs)

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        start = time.monotonic()
        if verbose:
            print(
                f"[LLM:{request_tag}] start attempt={attempt + 1}/{retries + 1} "
                f"model={resolved_model} timeout={timeout_seconds:.0f}s max_tokens={resolved_max_tokens}",
                flush=True,
            )
        request_kwargs: Dict[str, Any] = {
            "model": resolved_model,
            "messages": messages,
            "temperature": temperature,
            "top_p": resolved_top_p,
            "max_tokens": resolved_max_tokens,
            "timeout": timeout_seconds,
        }
        if resolved_seed is not None:
            request_kwargs["seed"] = resolved_seed
        try:
            response = client.chat.completions.create(**request_kwargs)
            elapsed = time.monotonic() - start
            if verbose:
                print(f"[LLM:{request_tag}] done elapsed={elapsed:.1f}s", flush=True)
            content = response.choices[0].message.content
            if content is None:
                return ""
            if isinstance(content, str):
                return content.strip()
            return str(content).strip()
        except Exception as exc:
            elapsed = time.monotonic() - start
            last_error = exc
            if verbose:
                print(
                    f"[LLM:{request_tag}] failed attempt={attempt + 1}/{retries + 1} "
                    f"elapsed={elapsed:.1f}s error={exc.__class__.__name__}: {exc}",
                    flush=True,
                )
            if attempt >= retries:
                if fail_soft:
                    fallback_reply = "{}" if request_tag in {"coding_single_event", "repair_event", "coding_candidate_select", "select_definition", "repair_trigger"} else "[]"
                    if verbose:
                        print(
                            f"[LLM:{request_tag}] fail-soft fallback after {attempt + 1} attempts: {fallback_reply}",
                            flush=True,
                        )
                    return fallback_reply
                raise
    if last_error is not None:
        if fail_soft:
            return "{}" if request_tag in {"coding_single_event", "repair_event", "coding_candidate_select", "select_definition", "repair_trigger"} else "[]"
        raise last_error
    return ""


def extract_trigger_event_hypotheses(
    text: str,
    event_definitions: str,
    *,
    exemplars: List[str] | None = None,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    planning_profile: str = "generic",
) -> List[Dict[str, Any]]:
    """Use an LLM to extract richer trigger hypotheses from text."""
    system_prompt = (
        "You are a code-generation agent for event extraction. Return only JSON."
    ) if planning_profile == "mapcoder" else (
        "You are the Planning Agent in a multi-agent event extraction system. "
        "Your job is to propose candidate event mentions from the text before argument extraction begins. "
        "Work mention-by-mention, keep event types aligned with the ontology definitions, and return strict JSON only."
    )
    exemplar_text = "\n\n".join(f"Example {idx + 1}: {example}" for idx, example in enumerate(exemplars or []))
    profile_instructions = ""
    if planning_profile == "casie":
        profile_instructions = (
            "CASIE planning hint:\n"
            "Prefer cyber-event trigger mentions such as breach, exposed, accessed, stolen, phishing, ransom, demanded, paid, released, patched, or gained access when they are explicitly present in the text. "
            "Avoid choosing standalone organization, product, platform, or software names as triggers when they only name participants or context.\n\n"
        )
    elif planning_profile == "casie_strict_trigger":
        profile_instructions = (
            "CASIE-specific trigger guidance:\n"
            "1. A trigger must denote the event mention itself, usually an eventive verb, verb phrase, or eventive nominal phrase.\n"
            "2. Do not use product names, organization names, person names, locations, platforms, brands, or document topics as triggers unless the text itself uses that span as the event mention.\n"
            "3. Do not use standalone entity mentions such as software names, company names, or victims as triggers when they only identify participants or context.\n"
            "4. Prefer explicit eventive expressions such as theft, breach, exposed, leaked, paid ransom, demanded payment, released patch, phishing email, or gained access over nearby entity names.\n"
            "5. If a candidate is only an entity or topic label and not an event mention, omit it.\n\n"
        )
    elif planning_profile == "genia":
        profile_instructions = (
            "GENIA biomedical event hints:\n"
            "Positive_regulation triggers express increase or activation, e.g. overexpression, activation, induction, enhanced, increased, high, critical.\n"
            "Negative_regulation triggers express decrease or inhibition, e.g. represses, suppress, inhibited, reduced, blocked, abrogated, decrease.\n"
            "Binding triggers express physical or molecular association, e.g. binds, binding, interaction, complex, associates.\n"
            "Gene_expression and Transcription triggers express expression or transcription events, e.g. expression, transcription, expressed, transcript.\n"
            "Localization triggers express movement or location, e.g. translocation, localization, located, recruitment.\n"
            "For the current schema, do not choose a trigger whose polarity or biology better matches another event type.\n\n"
        )
    user_prompt = (
        f"Event definitions:\n{event_definitions}\n\n"
        f"Text:\n{text}\n\n"
        "Generate candidate event-mention hypotheses as JSON. "
        "Each item must have trigger, event_type, confidence, and rationale. "
        "Use trigger text exactly from the text. Return only the JSON array."
    ) if planning_profile == "mapcoder" else (
        "Task:\n"
        "Use a DiCoRe-style two-step planning strategy for event extraction. First, be liberal and list all plausible event trigger mentions in the text. Second, conservatively map each trigger to exactly one event type from the provided definitions and drop triggers that cannot be mapped or are not actually event mentions.\n\n"
        "Core requirements:\n"
        "1. Each hypothesis must correspond to one specific event mention.\n"
        "2. The trigger must be copied verbatim from the text.\n"
        "3. Prefer event mentions themselves over participants, entities, topics, or background wording.\n"
        "4. Prefer the smallest exact trigger span that still expresses the event mention.\n"
        "5. Be recall-oriented when proposing possible triggers, but precision-oriented when assigning event types.\n"
        "6. If a trigger cannot be mapped to a provided event type, omit it.\n"
        "7. If the mapped event does not happen in the text, omit it.\n"
        "8. Do not use section titles, discourse markers, generic document words, or pure entity mentions as triggers unless the text itself uses them as eventive expressions.\n"
        "9. If both an eventive head word and a longer descriptive phrase are available, prefer the smallest exact eventive trigger.\n"
        "10. For GENIA-style biomedical events, prefer eventive verbs or eventive nominals over assay descriptions, participant names, or abstract topic labels.\n\n"
        "Output format:\n"
        "Return only a JSON array of objects with keys 'trigger', 'event_type', 'confidence', 'rationale', and optional 'selection_reason'.\n"
        "Use 'selection_reason' to briefly contrast the selected event type against likely confusable event types.\n\n"
        f"{profile_instructions}"
        f"Event definitions:\n{event_definitions}\n\n"
        f"Retrieved exemplars:\n{exemplar_text or 'None'}\n\n"
        f"Text:\n{text}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    reply = call_llm(
        messages,
        model=model,
        base_url=base_url,
        api_key=api_key,
        request_tag="planning_hypotheses",
        max_tokens=256 if planning_profile == "mapcoder" else 384,
    )
    data = _load_json_reply(reply)
    if not isinstance(data, list):
        return []

    hypotheses: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        trigger = item.get("trigger")
        event_type = item.get("event_type")
        confidence = item.get("confidence", 0.0)
        rationale = item.get("rationale", "")
        if not isinstance(trigger, str) or not isinstance(event_type, str):
            continue
        if isinstance(confidence, int):
            confidence = float(confidence)
        if not isinstance(confidence, float):
            confidence = 0.0
        confidence = min(1.0, max(0.0, confidence))
        if not isinstance(rationale, str):
            rationale = ""
        hypotheses.append(
            {
                "trigger": trigger,
                "event_type": event_type,
                "confidence": confidence,
                "rationale": rationale,
                "selection_reason": item.get("selection_reason", "") if isinstance(item.get("selection_reason", ""), str) else "",
            }
        )
    return hypotheses


def extract_trigger_event_pairs(
    text: str,
    event_definitions: str,
    *,
    exemplars: List[str] | None = None,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> List[Tuple[str, str]]:
    """Use an LLM to extract ``(trigger, event_type)`` pairs from text."""
    system_prompt = (
        "You are an assistant for event extraction. Given a piece of text and "
        "definitions of event types (as Python dataclasses), produce a JSON "
        "array of objects where each object has keys 'trigger' and 'event_type'."
    )
    exemplar_text = "\n\n".join(f"Example {idx + 1}: {example}" for idx, example in enumerate(exemplars or []))
    user_prompt = (
        f"Event definitions:\n{event_definitions}\n\n"
        f"Retrieved exemplars:\n{exemplar_text or 'None'}\n\n"
        f"Text:\n{text}\n\n"
        "Return only a JSON array of {'trigger': str, 'event_type': str} objects."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    reply = call_llm(messages, model=model, base_url=base_url, api_key=api_key, request_tag="planning_pairs", max_tokens=256)
    data = _load_json_reply(reply)
    if not isinstance(data, list):
        return []

    pairs: List[Tuple[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        trigger = item.get("trigger")
        evt_type = item.get("event_type")
        if isinstance(trigger, str) and isinstance(evt_type, str):
            pairs.append((trigger, evt_type))
    return pairs


def extract_arguments_for_event(
    text: str,
    trigger: str,
    event_type: str,
    role_names: List[str],
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    planning_profile: str = "generic",
) -> Dict[str, List[str]]:
    """Use an LLM to extract event arguments as a JSON object."""
    role_list = ", ".join(role_names)
    event_guidance = _get_event_specific_guidance(event_type, planning_profile)
    normalized_text = " ".join(text.split())
    normalized_trigger = " ".join(trigger.split())
    trigger_idx = normalized_text.lower().find(normalized_trigger.lower()) if normalized_trigger else -1
    if trigger_idx >= 0:
        local_start = max(0, trigger_idx - 260)
        local_end = min(len(normalized_text), trigger_idx + len(normalized_trigger) + 260)
        local_context = normalized_text[local_start:local_end]
    else:
        local_context = normalized_text[:600]
    argument_guidance = ""
    if planning_profile == "genia":
        argument_guidance = (
            "GENIA argument extraction constraints:\n"
            "- Use only spans from the same sentence as the trigger whenever possible; do not cross semicolons or clause boundaries.\n"
            "- Each role should contain at most one span. Use [] unless the span is explicitly and locally linked to this trigger.\n"
            "- Prefer short named biological entities: genes, proteins, protein complexes, cells, reporter constructs, domains, residues, promoters, or compartments.\n"
            "- Do not output full clauses, assay descriptions, experimental conditions, or phrases beginning with of/to/with/by/for/in/on/at/from/through.\n"
            "- Theme is the directly expressed, modified, localized, bound, or regulated biological participant.\n"
            "- Cause is only a clearly stated upstream regulator; for Positive_regulation and Negative_regulation, return [] for Cause if uncertain.\n"
            "- For Binding, fill Theme/Theme2 only when both participants are explicitly local to the binding trigger; otherwise prefer [] for uncertain participants.\n"
            "- For Gene_expression and Transcription, Theme is usually the expressed/transcribed gene, protein, mRNA, promoter, or reporter target, not the expression trigger itself.\n"
            "- For Localization, Theme is the moving/localized entity and Site/CSite is the location if explicitly stated.\n"
            "- For Phosphorylation or Protein_modification, Theme is the modified protein; Site/CSite is a residue or domain only if explicitly stated.\n"
        )
    elif planning_profile == "casie":
        argument_guidance = (
            "CASIE cyber argument extraction constraints:\n"
            "- Fill role names exactly as listed. Use [] only when the role is not expressed near this trigger.\n"
            "- Victim is the affected person, organization, account, device, system, network, data owner, or target.\n"
            "- Attacker is the actor causing the attack: hackers, attackers, criminals, fraudsters, ransomware actors, or named groups.\n"
            "- Tool is the malware, ransomware, phishing page/email, exploit, vulnerability weapon, app, virus, domain, or technical artifact used.\n"
            "- Attack-Pattern is the action/method/purpose phrase such as encrypted data, locked files, hijacked accounts, tricking users, or exploit vulnerabilities.\n"
            "- Compromised-Data is the data/information/accounts/passwords/records/files obtained, stolen, leaked, collected, or exposed.\n"
            "- Vulnerability is the flaw, bug, weakness, issue, CVE, vulnerability, loophole, or security problem.\n"
            "- Vulnerable_System is the affected product, device, platform, software, firmware, website, database, network, or system.\n"
            "- Releaser is the organization/person releasing or issuing a patch, update, advisory, or fix.\n"
            "- Patch is the update, fix, patch, advisory, release, signature, or mitigation being released/applied.\n"
            "- Discoverer is the person, organization, researcher, vendor, or team that reported, found, revealed, identified, or disclosed a vulnerability.\n"
            "- Capabilities and Issues-Addressed may be longer verb phrases if the gold role describes what the vulnerability permits or what the patch addresses.\n"
            "- Price, Payment-Method, Time, Place, CVE, Number roles should be filled with exact local spans when present.\n"
            "- Keep entity-like roles concise, but do not shorten multiword names such as Microsoft Word files, Positive Technologies, Cisco Policy Suite, or National Health Service.\n"
            "- Multiple fillers are allowed when the sentence explicitly lists parallel victims, attackers, data types, systems, or prices.\n"
        )
    system_prompt = (
        "You are a code-generation agent for event extraction. Return only JSON."
    ) if planning_profile == "mapcoder" else (
        "You are the Single-Event Extraction Agent in a multi-agent event extraction system. "
        "Your job is to extract argument spans for exactly one event mention given its trigger and schema roles. "
        "Return strict JSON only."
    )
    user_prompt = (
        f"Event type: {event_type}\n"
        f"Planning trigger: {trigger}\n"
        f"Roles: {role_list}\n"
        f"Local context:\n{local_context}\n\n"
        "Generate one event object as JSON. Return only one JSON object. "
        "Include key 'mention' plus every role name. Values for roles must be lists of exact spans from local context. "
        "Use the planning trigger as mention unless a nearby eventive span is clearly better. Use [] when a role is absent."
    ) if planning_profile == "mapcoder" else (
        "Task:\n"
        "Extract arguments for exactly one event mention anchored by the given trigger.\n\n"
        "Core requirements:\n"
        "1. Extract arguments only for this trigger mention.\n"
        "2. Every returned span must be copied verbatim from the text.\n"
        "3. Keep arguments local to the trigger mention when the text supports them.\n"
        "4. If the link between the trigger and a role filler is unclear, return an empty list for that role.\n"
        "5. Return all schema roles as keys, even when some values are empty lists.\n"
        "6. Prefer the smallest exact span that fills the role.\n"
        "7. Do not return broad event-description shells when a shorter entity-like or site-like span is supported.\n"
        "8. For theme-like roles, prefer the directly affected entity, molecule, gene, protein, complex, or reporter target over a longer process description when both are present.\n"
        "9. For cause-like roles, prefer the causal entity or molecular factor over experiment-description phrases such as overexpression of X or transfection of X when a shorter span is supported.\n"
        "10. For site-like roles, prefer concrete residues, domains, regions, promoters, elements, compartments, or cellular locations.\n"
        "11. For GENIA output, each role list should normally contain zero or one span; multiple spans are allowed only when the sentence explicitly enumerates parallel participants for that same role.\n"
        "12. Never include the trigger itself as an argument.\n\n"
        f"{argument_guidance}\n"
        "Trigger and event guidance:\n"
        f"{event_guidance or 'Use the provided trigger as the anchor and keep role fillers semantically compatible with this event type.'}\n\n"
        "Output format:\n"
        "Return exactly one JSON object whose keys are the role names and whose values are lists of strings.\n\n"
        f"Event type: {event_type}\n"
        f"Trigger: {trigger}\n"
        f"Roles: {role_list}\n"
        f"Local context around trigger:\n{local_context}\n\n"
        f"Text:\n{text}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    reply = call_llm(
        messages,
        model=model,
        base_url=base_url,
        api_key=api_key,
        request_tag="coding_single_event",
        max_tokens=384 if planning_profile == "mapcoder" else 512,
    )
    data = _load_json_reply(reply)
    normalized: Dict[str, List[str]] = {role: [] for role in role_names}
    if not isinstance(data, dict):
        return normalized
    if planning_profile == "mapcoder":
        mention = data.get("mention") or data.get("trigger")
        if isinstance(mention, str) and mention.strip():
            normalized["__mention"] = [mention.strip()]
    for role in role_names:
        value = data.get(role, [])
        if isinstance(value, str):
            normalized[role] = [value]
        elif isinstance(value, list):
            normalized[role] = [item for item in value if isinstance(item, str)]
    return normalized


def extract_mentions_for_event_type(
    text: str,
    event_type: str,
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    max_mentions: int = 8,
    planning_profile: str = "generic",
) -> List[str]:
    """Extract mention strings for one event type from text."""
    event_guidance = _get_event_specific_guidance(event_type, planning_profile)
    system_prompt = (
        "You are a code-generation agent for event extraction. Return only JSON."
    ) if planning_profile == "mapcoder" else (
        "You are the Multi-Mention Extraction Agent in a multi-agent event extraction system. "
        "Your job is to extract all trigger mentions for exactly one event type from one text and return strict JSON only."
    )
    user_prompt = (
        f"Event type: {event_type}\n"
        f"Text:\n{text}\n\n"
        "Return only a JSON array of trigger mention strings for this event type."
    ) if planning_profile == "mapcoder" else (
        "Task:\n"
        "Extract all supported trigger mentions of the given event type from the text.\n\n"
        "Rules:\n"
        "1. Return one string per event mention.\n"
        "2. Each mention must appear verbatim in the text.\n"
        "3. Prefer the smallest exact trigger phrase that still expresses the event mention.\n"
        "4. Do not return arguments, explanations, or event objects.\n"
        "5. Do not include mentions that are better mapped to another event type.\n"
        "6. Do not return section headers, discourse markers, or pure participant/entity names unless they are truly used as eventive triggers in the text.\n"
        "7. If both a broad phrase and a shorter eventive head are possible, prefer the shorter eventive head.\n"
        "8. If no mentions are clearly supported, return [].\n\n"
        "Event-specific trigger guidance:\n"
        f"{event_guidance or 'Choose only exact eventive trigger mentions for the requested event type.'}\n\n"
        "Output format:\n"
        "Return only a JSON array of strings.\n\n"
        f"Event type: {event_type}\n\n"
        f"Text:\n{text}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    reply = call_llm(
        messages,
        model=model,
        base_url=base_url,
        api_key=api_key,
        request_tag="coding_mentions",
        max_tokens=256,
    )
    data = _load_json_reply(reply)
    if not isinstance(data, list):
        return []
    mentions: List[str] = []
    seen: set[str] = set()
    for item in data[:max_mentions]:
        if not isinstance(item, str):
            continue
        cleaned = " ".join(item.split())
        lowered = cleaned.lower()
        if not cleaned or lowered in seen:
            continue
        seen.add(lowered)
        mentions.append(cleaned)
    return mentions


def extract_events_for_schema(
    text: str,
    event_type: str,
    role_names: List[str],
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    max_events: int = 8,
    planning_profile: str = "generic",
) -> List[Dict[str, List[str] | str]]:
    """Extract multiple events of the same schema from one text.

    Returns a list of dictionaries with a required ``mention`` field and optional
    role fields whose values are lists of strings.
    """
    role_list = ", ".join(role_names)
    event_guidance = _get_event_specific_guidance(event_type, planning_profile)
    system_prompt = (
        "You are a code-generation agent for event extraction. Return only JSON."
    ) if planning_profile == "mapcoder" else (
        "You are the Multi-Event Extraction Agent in a multi-agent event extraction system. "
        "Your job is to extract multiple mentions of the same event type from one text and keep each mention as a separate event object. "
        "Return strict JSON only."
    )
    user_prompt = (
        f"Event type: {event_type}\n"
        f"Roles: {role_list}\n"
        f"Text:\n{text}\n\n"
        "Generate event objects as JSON. Return only a JSON array. "
        "Each object must include mention and every role name. Role values must be lists of exact text spans. "
        "If no event is present, return []."
    ) if planning_profile == "mapcoder" else (
        "Task:\n"
        "Extract all supported mentions of the given event type from the text. Follow a DiCoRe-style policy: be liberal enough to cover every plausible mention of this event type, then be conservative when deciding whether each candidate truly belongs to the target type.\n\n"
        "Responsibilities:\n"
        "1. Return one object per event mention, not one object per document.\n"
        "2. Keep each mention separate and do not merge arguments across mentions.\n"
        "3. Extract arguments only when they are directly linked to that specific mention.\n\n"
        "Decision rules:\n"
        "1. The 'mention' value must be the trigger phrase exactly as it appears in the text.\n"
        "2. Prefer the smallest exact eventive trigger span; do not let section titles, discourse markers, or participant names act as triggers unless the text itself uses them as eventive expressions.\n"
        "3. Do not use reporting, notification, or background verbs as triggers unless they themselves express the target event mention.\n"
        "4. Do not use participants, entities, topics, methods, or states as triggers unless the wording itself denotes the target event.\n"
        "5. If a mention is plausible but maps better to another event type, omit it for this event type.\n"
        "6. Every argument span must be copied verbatim from the text.\n"
        "7. Prefer the smallest exact span that fills the role.\n"
        "8. Prefer local arguments that are directly attached to the mention; if the linkage is unclear, leave that role empty.\n"
        "9. For theme-like roles, prefer directly affected entities or molecular participants over broad process descriptions when both are available.\n"
        "10. For cause-like roles, prefer the causal molecule/factor over long experimental-operation phrases when the shorter causal span is supported.\n"
        "11. Return all schema roles for each event object, even when some values are empty lists.\n"
        "12. If no target event mentions are clearly supported after conservative type checking, return [].\n\n"
        "Event-specific trigger guidance:\n"
        f"{event_guidance or 'Choose only exact eventive trigger mentions for the requested event type.'}\n\n"
        "Output format:\n"
        "Return only a JSON array. Each item must look like {'mention': str, role_name: [str, ...], ...}.\n\n"
        f"Event type: {event_type}\n"
        f"Roles: {role_list}\n"
        f"Maximum number of events to return: {max_events}\n\n"
        f"Text:\n{text}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    reply = call_llm(
        messages,
        model=model,
        base_url=base_url,
        api_key=api_key,
        request_tag="coding_multi_event",
        max_tokens=640 if planning_profile == "mapcoder" else 1024,
    )
    data = _load_json_reply(reply)
    if not isinstance(data, list):
        return []

    normalized_events: List[Dict[str, List[str] | str]] = []
    for item in data[:max_events]:
        if not isinstance(item, dict):
            continue
        mention = item.get("mention") or item.get("trigger")
        if not isinstance(mention, str) or not mention.strip():
            continue
        event: Dict[str, List[str] | str] = {"mention": mention}
        for role in role_names:
            value = item.get(role, [])
            if isinstance(value, str):
                event[role] = [value]
            elif isinstance(value, list):
                event[role] = [x for x in value if isinstance(x, str)]
            else:
                event[role] = []
        normalized_events.append(event)
    return normalized_events


def select_event_definition(
    event_type: str,
    event_definitions: str,
    *,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> str:
    """Use an LLM to select the definition of a specific event type."""
    system_prompt = (
        "You are a helpful assistant for event ontology selection. "
        "Given a list of event definitions and the name of a target event type, "
        "return exactly the definition (including its class header and fields) "
        "that matches the target event type. If no matching definition is present, return an empty string."
    )
    user_prompt = (
        f"Event definitions:\n{event_definitions}\n\n"
        f"Target event type: {event_type}\n\n"
        "Return the matching definition verbatim."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    try:
        reply = call_llm(messages, model=model, base_url=base_url, api_key=api_key, request_tag="select_definition", max_tokens=256)
    except Exception:
        return ""
    _debug_log_llm_reply("select_definition", reply)
    return reply.strip()


def repair_trigger_hypothesis(
    text: str,
    event_type: str,
    current_trigger: str,
    verification_error: str,
    *,
    verification_info: Dict[str, Any] | None = None,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> str:
    """Use an LLM to repair a trigger hypothesis from verifier feedback."""
    system_prompt = (
        "You are the Trigger Repair Agent in a multi-agent event extraction system. "
        "Your job is to decide whether a trigger hypothesis should stay unchanged or be replaced with a better trigger span for the same event type. "
        "Return strict JSON only."
    )
    verifier_context = json.dumps(verification_info or {}, ensure_ascii=False)
    verifier_category = (verification_info or {}).get("category", "")
    user_prompt = (
        "Task:\n"
        "Repair the trigger only if verifier feedback shows that the current trigger span is wrong for this event type.\n\n"
        "Responsibilities:\n"
        "1. Keep the event type fixed.\n"
        "2. Change only the trigger span, not arguments.\n"
        "3. Prefer conservative edits; if the current trigger is still plausible, keep it.\n\n"
        "Decision rules:\n"
        "1. Return exactly one JSON object with key 'trigger'.\n"
        "2. The trigger must appear verbatim in the text.\n"
        "3. Prefer the smallest exact trigger span that directly evokes the event.\n"
        "4. If verifier category is trigger_not_in_text, replace the trigger with a supported span from the text when possible.\n"
        "5. If verifier category is event_type_mismatch, keep the event type fixed and choose a trigger that better matches that event type.\n"
        "6. If verifier category is missing_roles, argument_not_in_text, argument_matches_trigger, argument_type_mismatch, argument_not_locally_bound, or argument_crosses_clause_boundary, keep the trigger unchanged unless the text clearly shows the trigger itself is wrong.\n"
        "7. Never use a role filler as the trigger unless the text itself uses that exact span as the event mention.\n"
        "8. If uncertain, keep the current trigger.\n\n"
        "Output format:\n"
        "Return exactly one JSON object: {'trigger': str}.\n\n"
        f"Event type: {event_type}\n"
        f"Current trigger: {current_trigger}\n"
        f"Verifier feedback: {verification_error}\n"
        f"Structured verifier feedback: {verifier_context}\n"
        f"Verifier category: {verifier_category}\n\n"
        f"Text:\n{text}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    reply = call_llm(messages, model=model, base_url=base_url, api_key=api_key, request_tag="repair_trigger", max_tokens=128)
    data = _load_json_reply(reply)
    if not isinstance(data, dict):
        return current_trigger
    trigger = data.get("trigger")
    if isinstance(trigger, str) and trigger.strip():
        return trigger
    return current_trigger


def repair_event_object(
    text: str,
    event_type: str,
    trigger: str,
    role_names: List[str],
    current_arguments: Dict[str, List[str]],
    verification_error: str,
    *,
    verification_info: Dict[str, Any] | None = None,
    candidate_arguments: Dict[str, List[str]] | None = None,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> Dict[str, List[str]]:
    """Use an LLM to repair one event object's arguments from verifier feedback."""
    role_list = ", ".join(role_names)
    current_json = json.dumps(current_arguments, ensure_ascii=False)
    normalized_text = " ".join(text.split())
    normalized_trigger = " ".join(trigger.split())
    trigger_idx = normalized_text.lower().find(normalized_trigger.lower()) if normalized_trigger else -1
    if trigger_idx != -1:
        local_start = max(0, trigger_idx - 220)
        local_end = min(len(normalized_text), trigger_idx + len(normalized_trigger) + 220)
        local_context = normalized_text[local_start:local_end]
    else:
        local_context = normalized_text[:500]
    system_prompt = (
        "You are the Argument Repair Agent in a multi-agent event extraction system. "
        "Your job is to repair arguments for exactly one event mention using verifier feedback, nearby candidate spans, and the local text context. "
        "Return strict JSON only."
    )
    verifier_context = json.dumps(verification_info or {}, ensure_ascii=False)
    candidate_context = json.dumps(candidate_arguments or {}, ensure_ascii=False)
    verifier_category = (verification_info or {}).get("category", "")
    user_prompt = (
        "Task:\n"
        "Repair the arguments for one event mention while keeping them bound to the given trigger.\n\n"
        "Core requirements:\n"
        "1. Repair arguments only for this trigger mention.\n"
        "2. Use verifier feedback as the main signal for what to fix.\n"
        "3. Every returned span must appear verbatim in the text.\n"
        "4. Prefer local, directly supported spans when repairing arguments.\n"
        "5. If a role remains uncertain after repair, return an empty list for that role.\n"
        "6. Return all schema roles as keys, even if some values are empty lists.\n\n"
        "Output format:\n"
        "Return exactly one JSON object whose keys are the role names and whose values are lists of strings.\n\n"
        f"Event type: {event_type}\n"
        f"Trigger: {trigger}\n"
        f"Roles: {role_list}\n"
        f"Current arguments JSON: {current_json}\n"
        f"Verifier feedback: {verification_error}\n"
        f"Structured verifier feedback: {verifier_context}\n"
        f"Verifier category: {verifier_category}\n"
        f"Nearby candidate arguments JSON: {candidate_context}\n"
        f"Local context around trigger:\n{local_context}\n\n"
        f"Text:\n{text}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    reply = call_llm(messages, model=model, base_url=base_url, api_key=api_key, request_tag="repair_event", max_tokens=512)
    data = _load_json_reply(reply)
    normalized: Dict[str, List[str]] = {role: [] for role in role_names}
    if not isinstance(data, dict):
        return normalized
    for role in role_names:
        value = data.get(role, [])
        if isinstance(value, str):
            normalized[role] = [value]
        elif isinstance(value, list):
            normalized[role] = [item for item in value if isinstance(item, str)]
    return normalized
