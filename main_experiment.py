from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import re
import sys
import types
from collections import Counter
from pathlib import Path
from typing import Callable, Dict, List, Sequence

from tqdm.auto import tqdm

from aec_pipeline import AECPipeline
from retrieval_agent import RetrievalAgent
from event_schema import EventSchema, EventObject

ROOT_DIR = Path(__file__).resolve().parent
CODE_PROMPTS_DIR = ROOT_DIR / "utils" / "code_prompts"
CODE_EVAL_DIR = ROOT_DIR / "utils" / "code_evaluation"
PREPARE_DATASET_PATH = CODE_PROMPTS_DIR / "prepare_dataset.py"
EVENT_SCORER_PATH = CODE_EVAL_DIR / "events_scorer.py"

DATASET_TO_TASK: Dict[str, str] = {
    "ace05-en": "e2e",
    "casie": "e2e",
    "fewevent": "ed",
    "genia2011": "e2e",
    "speed": "ed",
}

TEXT_RE = re.compile(r'text = "(.*)"\n\n# The list called result', re.DOTALL)
CLASS_RE = re.compile(r"class\s+(\w+)\s*\(")
FIELD_RE = re.compile(r"^\s+([A-Za-z_][A-Za-z0-9_-]*)\s*:", re.MULTILINE)
MENTION_RE = re.compile(r"mention\s*=\s*(['\"])(.*?)\1", re.DOTALL)
STOP_WORDS = {
    "the",
    "a",
    "an",
    "of",
    "in",
    "and",
    "to",
    "for",
    "on",
    "with",
    "as",
    "by",
    "is",
    "was",
    "were",
    "be",
    "been",
    "are",
    "that",
    "this",
    "it",
    "also",
}
TRIGGER_PREFIX_STOPWORDS = {
    "will",
    "would",
    "should",
    "could",
    "can",
    "may",
    "might",
    "must",
    "shall",
    "do",
    "does",
    "did",
    "has",
    "have",
    "had",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
}


def ensure_prettytable_stub() -> None:
    if "prettytable" in sys.modules:
        return

    prettytable_module = types.ModuleType("prettytable")

    class PrettyTable:
        def __init__(self) -> None:
            self.field_names: List[str] = []
            self._rows: List[List[str]] = []

        def add_row(self, row: List[str]) -> None:
            self._rows.append(row)

        def __str__(self) -> str:
            lines = []
            if self.field_names:
                lines.append(" | ".join(map(str, self.field_names)))
            for row in self._rows:
                lines.append(" | ".join(map(str, row)))
            return "\n".join(lines)

        __repr__ = __str__

    prettytable_module.PrettyTable = PrettyTable
    sys.modules["prettytable"] = prettytable_module


def load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def resolve_dataset_name(dataset_name: str) -> str:
    dataset_aliases = {
        "genia2011": "genia2013",
    }
    return dataset_aliases.get(dataset_name, dataset_name)


def ensure_prepared_dataset(
    dataset_name: str,
    input_dir: Path,
    prepared_dir: Path,
    split: str,
    *,
    max_dev_test_samples_override: int | None = None,
) -> Path:
    resolved_name = resolve_dataset_name(dataset_name)
    dataset_dir = prepared_dir / dataset_name
    alias_dataset_dir = prepared_dir / resolved_name
    split_file = dataset_dir / f"{split}.json"
    alias_split_file = alias_dataset_dir / f"{split}.json"

    def _prepared_file_is_usable(candidate: Path) -> bool:
        if not candidate.exists():
            return False
        if max_dev_test_samples_override is None:
            return True
        try:
            with candidate.open(encoding="utf-8") as fh:
                prepared_samples = json.load(fh)
        except Exception:
            return False
        return isinstance(prepared_samples, list) and len(prepared_samples) >= max_dev_test_samples_override

    if _prepared_file_is_usable(split_file):
        return dataset_dir
    if _prepared_file_is_usable(alias_split_file):
        return alias_dataset_dir

    if str(CODE_PROMPTS_DIR) not in sys.path:
        sys.path.insert(0, str(CODE_PROMPTS_DIR))
    prepare_module = load_module("aec_prepare_dataset", PREPARE_DATASET_PATH)
    prepare_module.prepare_dataset(
        str(input_dir),
        dataset_name,
        add_negative_sample=False,
        annotate_schema=False,
        guidelines=None,
        output_dir=str(prepared_dir),
        nagative_sample_count=None,
        skip_train=dataset_name == "genia2011",
        max_dev_test_samples=max_dev_test_samples_override if max_dev_test_samples_override is not None else (200 if dataset_name == "genia2011" else None),
        positive_only=dataset_name == "genia2011",
        split_only=split if dataset_name == "genia2011" else None,
    )
    if split_file.exists():
        return dataset_dir
    return alias_dataset_dir


def load_samples(prepared_dir: Path, dataset_name: str, split: str, max_samples: int | None) -> List[dict]:
    resolved_name = resolve_dataset_name(dataset_name)
    split_file = prepared_dir / dataset_name / f"{split}.json"
    if not split_file.exists():
        split_file = prepared_dir / resolved_name / f"{split}.json"
    with split_file.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return data if max_samples is None else data[:max_samples]


def load_schema_roles(dataset_name: str) -> Dict[str, List[str]]:
    schema_path = ROOT_DIR / "utils" / "code_schema_generation" / "init_prompts" / f"{dataset_name}.txt"
    if not schema_path.exists():
        schema_path = ROOT_DIR / "utils" / "code_schema_generation" / "init_prompts" / f"{resolve_dataset_name(dataset_name)}.txt"
    schemas: Dict[str, List[str]] = {}
    current: str | None = None
    for line in schema_path.read_text(encoding="utf-8").splitlines():
        class_match = CLASS_RE.search(line)
        if class_match:
            current = canonical_event_class_name(class_match.group(1))
            schemas[current] = []
            continue
        if current is None:
            continue
        field_match = FIELD_RE.match(line)
        if field_match:
            field = field_match.group(1)
            if field != "mention":
                schemas[current].append(field)
        elif not line.strip():
            current = None
    return schemas


def canonical_event_class_name(name: str) -> str:
    aliases = {
        "Attack:Databreach": "Databreach",
        "Attack:Ransom": "Ransom",
        "Attack:Phishing": "Phishing",
        "Vulnerability-related:PatchVulnerability": "Patchvulnerability",
        "Vulnerability-related:DiscoverVulnerability": "Discovervulnerability",
        "PatchVulnerability": "Patchvulnerability",
        "DiscoverVulnerability": "Discovervulnerability",
    }
    return aliases.get(name, name)


def clean_event_type_name(event_type: str) -> str:
    raw_name = event_type.split("(", 1)[0].strip()
    canonical = canonical_event_class_name(raw_name)
    if canonical != raw_name:
        return canonical
    return raw_name.replace(":", "_").replace("-", "_").replace(".", "_")


def map_event_type_to_schema_name(event_type: str, schema_roles: Dict[str, List[str]]) -> str:
    cleaned = clean_event_type_name(event_type)
    if cleaned in schema_roles:
        return cleaned
    normalized_schema = {re.sub(r"[^a-z0-9]", "", key.lower()): key for key in schema_roles}
    normalized_cleaned = re.sub(r"[^a-z0-9]", "", cleaned.lower())
    if normalized_cleaned in normalized_schema:
        return normalized_schema[normalized_cleaned]
    parts = [part for part in re.split(r"_+", cleaned) if part]
    for start in range(1, len(parts)):
        candidate = "".join(part[:1].upper() + part[1:] for part in parts[start:])
        if candidate in schema_roles:
            return candidate
        normalized_candidate = re.sub(r"[^a-z0-9]", "", candidate.lower())
        if normalized_candidate in normalized_schema:
            return normalized_schema[normalized_candidate]
    return cleaned


def raw_event_to_fragment(event: dict, schema_roles: Dict[str, List[str]]) -> str:
    class_name = map_event_type_to_schema_name(str(event.get("event_type", "")), schema_roles)
    if class_name == "Protein_modification" and class_name not in schema_roles and "Phosphorylation" in schema_roles:
        class_name = "Phosphorylation"
    trigger = event.get("trigger", {}) if isinstance(event.get("trigger"), dict) else {}
    arg_values: Dict[str, List[str]] = {}
    for arg in event.get("arguments", []):
        if not isinstance(arg, dict):
            continue
        role = normalize_role_name(str(arg.get("role", "")))
        text = arg.get("text")
        if isinstance(text, str) and role:
            arg_values.setdefault(role, []).append(text)
    parts = [f"mention={str(trigger.get('text', ''))!r}"]
    for role in schema_roles.get(class_name, []):
        parts.append(f"{normalize_role_name(role)}={arg_values.get(normalize_role_name(role), [])!r}")
    return f"{class_name}({', '.join(parts)})"


def build_raw_e2e_output(sample: dict, schema_roles: Dict[str, List[str]]) -> str:
    fragments = [raw_event_to_fragment(event, schema_roles) for event in sample.get("event_mentions", []) if isinstance(event, dict)]
    return f"[{', '.join(fragments)}]" if fragments else "[]"


def load_raw_e2e_samples(input_dir: Path, dataset_name: str, split: str, max_samples: int | None) -> tuple[List[dict], Dict[str, List[str]]]:
    resolved_name = resolve_dataset_name(dataset_name)
    split_file = input_dir / resolved_name / "split1" / f"{split}.json"
    if not split_file.exists():
        split_file = input_dir / dataset_name / "split1" / f"{split}.json"
    schema_roles = load_schema_roles(dataset_name)
    raw_samples = [json.loads(line) for line in split_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    prepared_samples = []
    for sample in raw_samples:
        text = sample.get("text", "")
        if not isinstance(text, str):
            text = ""
        prepared_samples.append(
            {
                "input": text,
                "output": build_raw_e2e_output(sample, schema_roles),
                "raw": sample,
            }
        )
    return (prepared_samples if max_samples is None else prepared_samples[:max_samples]), schema_roles


def build_raw_e2e_prompt(text: str, schema_roles: Dict[str, List[str]]) -> str:
    blocks = ["# The following lines describe all event task definitions", ""]
    for class_name, roles in schema_roles.items():
        blocks.append("@dataclass")
        blocks.append(f"class {class_name}(Event):")
        blocks.append("    mention: str")
        for role in roles:
            blocks.append(f"    {role}: List")
        blocks.append("")
    blocks.append("# This is the text to analyze")
    blocks.append(f"text = {text!r}")
    blocks.append("")
    blocks.append("# The list called result should contain all event instances in the text:")
    blocks.append("result = ")
    return "\n".join(blocks)


def build_raw_e2e_prediction(
    pipeline: AECPipeline,
    schema_roles: Dict[str, List[str]],
    text: str,
    gold_output: str,
    use_llm_plan: bool,
    use_llm_coding: bool,
    *,
    dataset_name: str,
    planning_profile: str,
    trigger_adapter: str,
    output_adapter: str,
    normalize_triggers: bool,
    doc_argument_dedup: bool = False,
    schema_mode: str = "all",
) -> tuple[str, List[dict], Dict[str, object]]:
    if gold_output.strip() == "[]":
        return "[]", [], {}
    if schema_mode == "gold":
        class_names = sorted({
            map_event_type_to_schema_name(event_type, schema_roles)
            for event_type in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\(mention=", gold_output)
        })
    else:
        class_names = list(schema_roles.keys())
    fragments: List[str] = []
    traces: List[dict] = []
    aggregate = {
        "hypothesis_count": 0,
        "validated_event_count": 0,
        "verified_pass_count": 0,
        "verified_fail_count": 0,
        "repair_attempt_count": 0,
        "repair_changed_count": 0,
        "trigger_normalization_count": 0,
        "verifier_categories": {},
        "repair_routes": {},
        "repair_outcomes": {},
    }
    seen_fragments: set[str] = set()
    for class_name in class_names:
        roles = schema_roles.get(class_name)
        if roles is None:
            continue
        prediction, trace, summary = build_prediction(
            pipeline=pipeline,
            class_name=class_name,
            role_names=roles,
            text=text,
            gold_output=gold_output,
            use_llm_plan=use_llm_plan,
            use_llm_coding=use_llm_coding,
            dataset_name=dataset_name,
            planning_profile=planning_profile,
            trigger_adapter=trigger_adapter,
            output_adapter=output_adapter,
            normalize_triggers=normalize_triggers,
            doc_argument_dedup=doc_argument_dedup,
            allow_fallback=False,
        )
        traces.append({"event_type": class_name, "trace": trace, "summary": summary})
        if prediction != "[]":
            inner = prediction.strip()[1:-1].strip()
            if inner:
                for fragment in re.split(r"\),\s*(?=[A-Za-z_][A-Za-z0-9_]*\()", inner):
                    if fragment and not fragment.endswith(")"):
                        fragment = fragment + ")"
                    if fragment and fragment not in seen_fragments:
                        seen_fragments.add(fragment)
                        fragments.append(fragment)
        for key in ["hypothesis_count", "validated_event_count", "verified_pass_count", "verified_fail_count", "repair_attempt_count", "repair_changed_count", "trigger_normalization_count"]:
            aggregate[key] += int(summary.get(key, 0))
        for bucket_name in ["verifier_categories", "repair_routes", "repair_outcomes"]:
            bucket = summary.get(bucket_name, {})
            if isinstance(bucket, dict):
                for name, value in bucket.items():
                    aggregate[bucket_name][name] = aggregate[bucket_name].get(name, 0) + int(value)
    return (f"[{', '.join(fragments)}]" if fragments else "[]"), traces, aggregate


def build_example_db(prepared_dir: Path, dataset_name: str, *, split: str = "train", max_examples_per_type: int = 64) -> Dict[str, List[str]]:
    resolved_name = resolve_dataset_name(dataset_name)
    split_file = prepared_dir / dataset_name / f"{split}.json"
    if not split_file.exists():
        split_file = prepared_dir / resolved_name / f"{split}.json"
    if not split_file.exists():
        return {}

    with split_file.open(encoding="utf-8") as fh:
        data = json.load(fh)

    example_db: Dict[str, List[str]] = {}
    seen_by_type: Dict[str, set[str]] = {}
    for sample in data:
        if not isinstance(sample, dict):
            continue
        prompt = sample.get("input")
        output = sample.get("output")
        if not isinstance(prompt, str) or not isinstance(output, str):
            continue
        try:
            class_name, _, text = parse_prompt(prompt)
        except ValueError:
            continue
        if output.strip() == "[]":
            continue

        triggers: List[str] = []
        seen_triggers: set[str] = set()
        for _, mention in MENTION_RE.findall(output):
            trigger = " ".join(mention.split())
            if not trigger or trigger.lower() in seen_triggers:
                continue
            if trigger.lower() not in text.lower():
                continue
            seen_triggers.add(trigger.lower())
            triggers.append(trigger)
            if len(triggers) >= 8:
                break
        if not triggers:
            continue

        bucket = example_db.setdefault(class_name, [])
        if len(bucket) >= max_examples_per_type:
            continue
        seen = seen_by_type.setdefault(class_name, set())
        snippet = " ".join(text.split())[:900]
        trigger_list = "; ".join(triggers)
        exemplar = (
            f"Event type: {class_name}\n"
            f"Text snippet: {snippet}\n"
            f"Gold trigger mentions: {trigger_list}"
        )
        normalized = " ".join(exemplar.split()).lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        bucket.append(exemplar)
    return example_db


def parse_prompt(prompt: str) -> tuple[str, List[str], str]:
    class_match = CLASS_RE.search(prompt)
    if class_match is None:
        raise ValueError("Could not find event class in prompt")
    class_name = class_match.group(1)

    text_match = TEXT_RE.search(prompt)
    if text_match is None:
        raise ValueError("Could not extract text from prompt")
    text = text_match.group(1)

    schema_block = prompt.split("# This is the text to analyze", 1)[0]
    fields = [field for field in FIELD_RE.findall(schema_block) if field != "mention"]
    return class_name, fields, text


def normalize_role_name(role_name: str) -> str:
    return role_name.replace("-", "_").replace(".", "_").lower()


def fallback_trigger(text: str) -> str | None:
    tokens = re.findall(r"\b\w+\b", text)
    for token in tokens:
        if token.lower() not in STOP_WORDS:
            return token
    return tokens[0] if tokens else None


def trim_trigger_for_ed(trigger: str) -> str:
    words = trigger.split()
    while len(words) > 1 and words[0].lower() in TRIGGER_PREFIX_STOPWORDS:
        words = words[1:]
    return " ".join(words) if words else trigger


def event_to_prediction_fragment(class_name: str, role_names: Sequence[str], event: EventObject, *, trim_trigger: bool = False) -> str:
    mention = trim_trigger_for_ed(event.trigger) if trim_trigger else event.trigger
    arg_parts = [f"mention={mention!r}"]
    for role_name in role_names:
        values = event.arguments.get(role_name, [])
        arg_parts.append(f"{normalize_role_name(role_name)}={values!r}")
    return f"{class_name}({', '.join(arg_parts)})"


CASIE_TRIGGER_HEADS = {
    "breach", "breached", "compromise", "compromised", "access", "accessed", "exposed", "expose",
    "stolen", "steal", "steals", "stole", "leaked", "leak", "phishing", "phish", "defrauded",
    "fraud", "ransom", "ransomed", "demanded", "demand", "paid", "pay", "payment", "encrypts",
    "encrypted", "locked", "decrypt", "released", "release", "patched", "patch", "fixed", "fix",
    "update", "announced", "revealed", "discovered", "affects", "exploited",
}
CASIE_WEAK_TRIGGER_HEADS = {
    "due", "few", "random", "starting", "started", "resulted", "resulted in", "san",
}
CASIE_TRIGGER_PREFIX_PATTERNS = {
    "Patchvulnerability": [
        "has been {t}", "have been {t}", "had been {t}", "was {t}", "were {t}", "is {t}", "are {t}",
        "has {t}", "have {t}", "had {t}", "will push that {t}",
    ],
    "Discovervulnerability": [
        "have {t}", "has {t}", "had {t}", "was {t}", "were {t}", "been {t}", "are {t}", "is {t}",
    ],
    "Databreach": ["a {t}", "the {t}", "was {t}", "were {t}", "data {t}"],
    "Ransom": ["a {t}", "the {t}", "ransomware {t}"],
    "Phishing": ["a {t}", "the {t}"],
}
CASIE_TRIGGER_SUFFIX_PATTERNS = {
    "Phishing": ["{t} as", "{t} to be"],
    "Ransom": ["{t} a ransom", "{t} the ransom", "{t} for payment", "{t} for a ransom", "{t} payment", "{t} demands", "{t} demand", "{t} attack", "{t} attacks", "{t} campaign"],
    "Databreach": ["{t} leak", "{t} breach"],
}


def _copy_event_with_trigger(event: EventObject, trigger: str) -> EventObject:
    try:
        return event.copy(update={"trigger": trigger})
    except Exception:
        return EventObject(event_type=event.event_type, trigger=trigger, arguments=event.arguments)


def _locate_phrase_case_insensitive(text: str, phrase: str) -> str | None:
    match = re.search(re.escape(phrase), text, flags=re.IGNORECASE)
    if not match:
        return None
    return text[match.start():match.end()]


def _expand_casie_trigger_span(trigger: str, text: str, event_type: str) -> str:
    normalized_trigger = " ".join(trigger.split()).strip()
    if not normalized_trigger:
        return normalized_trigger
    lower_text = " ".join(text.split())
    lower_trigger = normalized_trigger.lower()
    prefix_patterns = CASIE_TRIGGER_PREFIX_PATTERNS.get(event_type, [])
    suffix_patterns = CASIE_TRIGGER_SUFFIX_PATTERNS.get(event_type, [])
    for template in prefix_patterns:
        phrase = template.format(t=lower_trigger)
        located = _locate_phrase_case_insensitive(lower_text, phrase)
        if located:
            return located
    for template in suffix_patterns:
        phrase = template.format(t=lower_trigger)
        located = _locate_phrase_case_insensitive(lower_text, phrase)
        if located:
            return located
    return normalized_trigger


def _normalize_casie_trigger_span(trigger: str) -> str:
    words = re.findall(r"\b[\w'-]+\b", trigger)
    if not words:
        return trigger
    lowered = [word.lower() for word in words]
    joined_lower = " ".join(lowered)

    phrase_candidates = [
        ("gained access", "gained access"),
        ("gaining access", "gaining access"),
        ("gain access", "gain access"),
        ("data breach", "data breach"),
        ("ransom payment", "ransom payment"),
        ("pay the ransom", "pay the ransom"),
        ("paid the ransom", "paid the ransom"),
        ("firmware update", "update"),
    ]
    for phrase, replacement in phrase_candidates:
        if phrase in joined_lower:
            if replacement == phrase:
                start = joined_lower.find(phrase)
                return trigger[start : start + len(phrase)] if start >= 0 else replacement
            return replacement

    if len(words) <= 2 and joined_lower not in CASIE_WEAK_TRIGGER_HEADS:
        return trigger

    for original, lower in zip(words, lowered):
        if lower in CASIE_TRIGGER_HEADS:
            return original
    return trigger


def _canonical_text_span(span: str, text: str) -> str:
    cleaned = " ".join(span.split())
    if not cleaned:
        return cleaned
    normalized_text = " ".join(text.split())
    match = re.search(re.escape(cleaned), normalized_text, flags=re.IGNORECASE)
    if match:
        return normalized_text[match.start():match.end()]
    return cleaned


def canonicalize_event_spans(event: EventObject, *, text: str) -> EventObject:
    canonical_trigger = _canonical_text_span(event.trigger, text)
    canonical_arguments: Dict[str, List[str]] = {}
    for role, values in event.arguments.items():
        canonical_arguments[role] = [_canonical_text_span(value, text) for value in values]
    return EventObject(event_type=event.event_type, trigger=canonical_trigger, arguments=canonical_arguments)


def normalize_trigger_for_dataset(event: EventObject, *, text: str, dataset_name: str | None) -> tuple[EventObject, Dict[str, str] | None]:
    if dataset_name != "casie":
        return event, None
    old_trigger = event.trigger.strip()
    if not old_trigger:
        return event, None
    shrunk_trigger = _normalize_casie_trigger_span(old_trigger).strip()
    expanded_trigger = _expand_casie_trigger_span(shrunk_trigger, text, event.event_type).strip()
    candidate_trigger = expanded_trigger or shrunk_trigger or old_trigger
    if not candidate_trigger or candidate_trigger == old_trigger:
        return event, None
    if candidate_trigger.lower() not in text.lower():
        return event, None
    normalized = _copy_event_with_trigger(event, candidate_trigger)
    return normalized, {"from": old_trigger, "to": candidate_trigger, "route": "casie_trigger_anchor_alignment"}


def deduplicate_doc_level_arguments(events: List[EventObject]) -> List[EventObject]:
    seen: set[tuple[str, str, str]] = set()
    deduped_events: List[EventObject] = []
    for event in events:
        new_arguments: Dict[str, List[str]] = {}
        kept_any = False
        for role, values in event.arguments.items():
            kept_values: List[str] = []
            for value in values:
                key = (event.event_type, role.lower(), " ".join(value.split()).lower())
                if key in seen:
                    continue
                seen.add(key)
                kept_values.append(value)
            new_arguments[role] = kept_values
            if kept_values:
                kept_any = True
        if kept_any or not deduped_events:
            deduped_events.append(EventObject(event_type=event.event_type, trigger=event.trigger, arguments=new_arguments))
    return deduped_events


def build_prediction(
    pipeline: AECPipeline,
    class_name: str,
    role_names: Sequence[str],
    text: str,
    gold_output: str,
    use_llm_plan: bool = False,
    use_llm_coding: bool = False,
    *,
    dataset_name: str | None = None,
    planning_profile: str = "generic",
    trigger_adapter: str = "none",
    output_adapter: str = "none",
    normalize_triggers: bool = False,
    doc_argument_dedup: bool = False,
    allow_fallback: bool = True,
) -> tuple[str, List[dict], Dict[str, object]]:
    if gold_output.strip() == "[]":
        return "[]", [], {}

    schema = EventSchema(event_type=class_name, roles={role: str for role in role_names})
    pipeline.planning_profile = planning_profile
    pipeline.trigger_adapter = trigger_adapter
    pipeline.output_adapter = output_adapter
    pipeline.coding_agent.planning_profile = planning_profile
    pipeline.coding_agent.output_adapter = output_adapter
    pipeline.planning_agent.trigger_adapter = trigger_adapter
    events = pipeline.run_many(
        text=text,
        schema=schema,
        dataset="user_defined",
        event_type=class_name,
        use_llm_plan=use_llm_plan,
        use_llm_coding=use_llm_coding,
    )
    trim_trigger = DATASET_TO_TASK.get(dataset_name or "", "") == "ed"
    events = [canonicalize_event_spans(event, text=text) for event in events]
    normalization_changes = []
    if normalize_triggers and events:
        normalized_events = []
        for event in events:
            normalized_event, change = normalize_trigger_for_dataset(event, text=text, dataset_name=dataset_name)
            normalized_events.append(normalized_event)
            if change is not None:
                normalization_changes.append(change)
        events = normalized_events
        if normalization_changes:
            pipeline.last_run_summary = dict(pipeline.last_run_summary)
            pipeline.last_run_summary["trigger_normalization_count"] = len(normalization_changes)
            pipeline.last_run_summary["trigger_normalizations"] = normalization_changes
            pipeline.last_run_trace.append({"stage": "trigger_normalization", "changes": normalization_changes})
    if doc_argument_dedup and events:
        deduped_events = deduplicate_doc_level_arguments(events)
        removed = max(0, sum(sum(len(v) for v in event.arguments.values()) for event in events) - sum(sum(len(v) for v in event.arguments.values()) for event in deduped_events))
        events = deduped_events
        if removed:
            pipeline.last_run_summary = dict(pipeline.last_run_summary)
            pipeline.last_run_summary["doc_argument_dedup_removed"] = int(pipeline.last_run_summary.get("doc_argument_dedup_removed", 0)) + removed
            pipeline.last_run_trace.append({"stage": "doc_argument_dedup", "removed": removed})
    if not events:
        if not allow_fallback:
            return "[]", pipeline.last_run_trace, pipeline.last_run_summary
        trigger = fallback_trigger(text)
        if not trigger:
            return "[]", pipeline.last_run_trace, pipeline.last_run_summary
        fallback_event = EventObject(
            event_type=class_name,
            trigger=trigger,
            arguments={role: [] for role in role_names},
        )
        return (
            f"[{event_to_prediction_fragment(class_name, role_names, fallback_event, trim_trigger=trim_trigger)}]",
            pipeline.last_run_trace,
            pipeline.last_run_summary,
        )

    fragments = [event_to_prediction_fragment(class_name, role_names, event, trim_trigger=trim_trigger) for event in events]
    return f"[{', '.join(fragments)}]", pipeline.last_run_trace, pipeline.last_run_summary


def evaluate_predictions(dataset_name: str, records: List[dict]) -> dict:
    ensure_prettytable_stub()
    if str(CODE_EVAL_DIR) not in sys.path:
        sys.path.insert(0, str(CODE_EVAL_DIR))
    scorer_module = load_module("aec_events_scorer", EVENT_SCORER_PATH)

    task = DATASET_TO_TASK[dataset_name]
    metric_fn: Callable[[List[dict]], dict]
    if task == "ed":
        metric_fn = scorer_module.micro_ed_scores
    elif task == "e2e":
        metric_fn = scorer_module.micro_e2e_scores
    else:
        metric_fn = scorer_module.micro_eae_scores
    try:
        return metric_fn(records)
    except Exception as exc:
        if task == "ed":
            print(f"[Eval:{dataset_name}] official ED scorer failed ({exc.__class__.__name__}: {exc}); using raw_e2e ED fallback evaluator.", flush=True)
            return compute_fallback_ed_metrics(records)
        raise


EVENT_FRAGMENT_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\(mention=(['\"])(.*?)\2(.*?)\)")
ARGUMENT_FIELD_RE = re.compile(r",\s*([A-Za-z0-9_]+)=((?:\[[^\]]*\])|(?:'[^']*')|(?:\"[^\"]*\")|(?:None))")


def compute_fallback_ed_metrics(records: List[dict]) -> Dict[str, object]:
    gold_id: Counter = Counter()
    pred_id: Counter = Counter()
    gold_cls: Counter = Counter()
    pred_cls: Counter = Counter()
    for record in records:
        for event_type, _quote, trigger, _body in EVENT_FRAGMENT_RE.findall(str(record.get("Label", ""))):
            normalized_trigger = _normalize_metric_span(trigger)
            if normalized_trigger:
                gold_id[normalized_trigger] += 1
                gold_cls[(event_type, normalized_trigger)] += 1
        for event_type, _quote, trigger, _body in EVENT_FRAGMENT_RE.findall(str(record.get("Prediction", ""))):
            normalized_trigger = _normalize_metric_span(trigger)
            if normalized_trigger:
                pred_id[normalized_trigger] += 1
                pred_cls[(event_type, normalized_trigger)] += 1
    id_tp, id_fp, id_fn = _counter_prf(gold_id, pred_id)
    cls_tp, cls_fp, cls_fn = _counter_prf(gold_cls, pred_cls)
    id_scores = _format_prf(id_tp, id_fp, id_fn)
    cls_scores = _format_prf(cls_tp, cls_fp, cls_fn)
    return {
        "trigger_id_precision": float(id_scores["precision"]),
        "trigger_id_recall": float(id_scores["recall"]),
        "trigger_id_f1": float(id_scores["f1"]),
        "event_id_precision": float(cls_scores["precision"]),
        "event_id_recall": float(cls_scores["recall"]),
        "event_id_f1": float(cls_scores["f1"]),
        "arg_id_precision": 0.0,
        "arg_id_recall": 0.0,
        "arg_id_f1": 0.0,
        "arg_cls_precision": 0.0,
        "arg_cls_recall": 0.0,
        "arg_cls_f1": 0.0,
        "hallucinations": [],
        "fallback_evaluator": "raw_e2e_ed_fragment_counter",
        "trigger_id_counts": {"tp": id_tp, "fp": id_fp, "fn": id_fn},
        "event_id_counts": {"tp": cls_tp, "fp": cls_fp, "fn": cls_fn},
    }


def _normalize_metric_span(value: str) -> str:
    value = value.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value.strip().strip("\"'")).lower()


def _parse_event_argument_tuples(output: str) -> List[tuple[str, str, str, str]]:
    tuples: List[tuple[str, str, str, str]] = []
    for event_match in EVENT_FRAGMENT_RE.finditer(output or ""):
        event_type, _, trigger, body = event_match.groups()
        normalized_trigger = _normalize_metric_span(trigger)
        for role_match in ARGUMENT_FIELD_RE.finditer(body):
            role, raw_value = role_match.groups()
            values: List[object] = []
            try:
                if raw_value.startswith("["):
                    parsed = ast.literal_eval(raw_value)
                    values = parsed if isinstance(parsed, list) else []
                elif raw_value[:1] in {"'", '"'}:
                    values = [ast.literal_eval(raw_value)]
            except Exception:
                values = []
            for value in values:
                if isinstance(value, str) and value.strip():
                    tuples.append((event_type, normalized_trigger, role, _normalize_metric_span(value)))
    return tuples


def _counter_prf(gold: Counter, pred: Counter) -> tuple[int, int, int]:
    tp = sum((gold & pred).values())
    fp = sum((pred - gold).values())
    fn = sum((gold - pred).values())
    return tp, fp, fn


def _format_prf(tp: int, fp: int, fn: int) -> Dict[str, float | int]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1, "tp": tp, "fp": fp, "fn": fn}


def compute_trigger_agnostic_argument_metrics(records: List[dict]) -> Dict[str, Dict[str, float | int]]:
    totals = {
        "doc_event_argument_identification": [0, 0, 0],
        "doc_event_argument_classification": [0, 0, 0],
        "doc_argument_span_only": [0, 0, 0],
        "trigger_sensitive_argument_identification": [0, 0, 0],
    }
    for record in records:
        gold_tuples = _parse_event_argument_tuples(str(record.get("Label", "")))
        pred_tuples = _parse_event_argument_tuples(str(record.get("Prediction", "")))
        comparisons = {
            "doc_event_argument_identification": (
                Counter((event_type, span) for event_type, _trigger, _role, span in gold_tuples),
                Counter((event_type, span) for event_type, _trigger, _role, span in pred_tuples),
            ),
            "doc_event_argument_classification": (
                Counter((event_type, role, span) for event_type, _trigger, role, span in gold_tuples),
                Counter((event_type, role, span) for event_type, _trigger, role, span in pred_tuples),
            ),
            "doc_argument_span_only": (
                Counter(span for _event_type, _trigger, _role, span in gold_tuples),
                Counter(span for _event_type, _trigger, _role, span in pred_tuples),
            ),
            "trigger_sensitive_argument_identification": (
                Counter((event_type, trigger, span) for event_type, trigger, _role, span in gold_tuples),
                Counter((event_type, trigger, span) for event_type, trigger, _role, span in pred_tuples),
            ),
        }
        for name, (gold_counter, pred_counter) in comparisons.items():
            tp, fp, fn = _counter_prf(gold_counter, pred_counter)
            totals[name][0] += tp
            totals[name][1] += fp
            totals[name][2] += fn
    return {name: _format_prf(tp, fp, fn) for name, (tp, fp, fn) in totals.items()}


def build_primary_metrics(official_metrics: Dict[str, object], trigger_agnostic_metrics: Dict[str, Dict[str, float | int]]) -> Dict[str, float]:
    doc_ai = trigger_agnostic_metrics.get("doc_event_argument_identification", {})
    doc_ac = trigger_agnostic_metrics.get("doc_event_argument_classification", {})
    return {
        "trigger_id_precision": float(official_metrics.get("trigger_id_precision", 0.0)),
        "trigger_id_recall": float(official_metrics.get("trigger_id_recall", 0.0)),
        "trigger_id_f1": float(official_metrics.get("trigger_id_f1", 0.0)),
        "event_id_precision": float(official_metrics.get("event_id_precision", 0.0)),
        "event_id_recall": float(official_metrics.get("event_id_recall", 0.0)),
        "event_id_f1": float(official_metrics.get("event_id_f1", 0.0)),
        "arg_id_precision": float(doc_ai.get("precision", 0.0)),
        "arg_id_recall": float(doc_ai.get("recall", 0.0)),
        "arg_id_f1": float(doc_ai.get("f1", 0.0)),
        "arg_cls_precision": float(doc_ac.get("precision", 0.0)),
        "arg_cls_recall": float(doc_ac.get("recall", 0.0)),
        "arg_cls_f1": float(doc_ac.get("f1", 0.0)),
    }


def build_derived_analytics(aggregate_summary: Dict[str, object]) -> Dict[str, float]:
    samples = max(int(aggregate_summary.get("samples", 0)), 1)
    verified_fail_count = int(aggregate_summary.get("verified_fail_count", 0))
    verified_pass_count = int(aggregate_summary.get("verified_pass_count", 0))
    repair_outcomes = aggregate_summary.get("repair_outcomes", {})
    repair_routes = aggregate_summary.get("repair_routes", {})
    if not isinstance(repair_outcomes, dict):
        repair_outcomes = {}
    if not isinstance(repair_routes, dict):
        repair_routes = {}
    total_repairs = sum(int(value) for value in repair_outcomes.values())
    total_routes = sum(int(value) for value in repair_routes.values())
    total_verifications = verified_pass_count + verified_fail_count
    return {
        "avg_hypotheses_per_sample": round(int(aggregate_summary.get("hypothesis_count", 0)) / samples, 4),
        "avg_validated_events_per_sample": round(int(aggregate_summary.get("validated_event_count", 0)) / samples, 4),
        "avg_verify_failures_per_sample": round(verified_fail_count / samples, 4),
        "verify_pass_rate": round(verified_pass_count / total_verifications, 4) if total_verifications else 0.0,
        "repair_attempts_per_sample": round(int(aggregate_summary.get("repair_attempt_count", 0)) / samples, 4),
        "repair_change_rate": round(int(aggregate_summary.get("repair_changed_count", 0)) / int(aggregate_summary.get("repair_attempt_count", 0)), 4) if int(aggregate_summary.get("repair_attempt_count", 0)) else 0.0,
        "repair_resolution_rate": round(int(repair_outcomes.get("resolved", 0)) / total_repairs, 4) if total_repairs else 0.0,
        "repair_shift_rate": round(int(repair_outcomes.get("shifted", 0)) / total_repairs, 4) if total_repairs else 0.0,
        "trigger_route_share": round(int(repair_routes.get("trigger", 0)) / total_routes, 4) if total_routes else 0.0,
        "argument_route_share": round(int(repair_routes.get("argument", 0)) / total_routes, 4) if total_routes else 0.0,
    }


def build_dominant_summary(aggregate_summary: Dict[str, object]) -> Dict[str, object]:
    def _top_entry(bucket: object) -> Dict[str, object]:
        if not isinstance(bucket, dict) or not bucket:
            return {"name": None, "count": 0}
        name, count = max(bucket.items(), key=lambda item: int(item[1]))
        return {"name": name, "count": int(count)}

    return {
        "top_verifier_category": _top_entry(aggregate_summary.get("verifier_categories", {})),
        "dominant_repair_route": _top_entry(aggregate_summary.get("repair_routes", {})),
        "dominant_repair_outcome": _top_entry(aggregate_summary.get("repair_outcomes", {})),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the main AEC experiment pipeline on a prepared split.")
    parser.add_argument("--dataset_name", required=True, choices=sorted(DATASET_TO_TASK.keys()))
    parser.add_argument("--split", default="test", choices=["train", "dev", "test"])
    parser.add_argument("--input_dir", default=str(ROOT_DIR / "datasets" / "processed_data"))
    parser.add_argument("--prepared_dir", default=str(ROOT_DIR / "demo_result" / "prepared_prompts"))
    parser.add_argument("--paper_eval", action="store_true", help="Use the paper-style uniformly sampled evaluation splits from datasets/paper_eval_splits.")
    parser.add_argument("--output_file", default="")
    parser.add_argument("--max_samples", type=int, default=200)
    parser.add_argument("--paper_eval_prepared_dir", default=str(ROOT_DIR / "demo_result" / "prepared_prompts_paper_eval"), help="Prepared prompt cache directory for paper_eval mode.")
    parser.add_argument("--show_progress", action="store_true", help="Compatibility flag; progress is shown by default.")
    parser.add_argument("--no_progress", action="store_true", help="Disable the progress bar while processing samples.")
    parser.add_argument("--skip_prepare", action="store_true")
    parser.add_argument("--use_llm_plan", action="store_true")
    parser.add_argument("--use_llm_coding", action="store_true")
    parser.add_argument("--use_prepared_exemplars", action="store_true", help="Use compact trigger exemplars built from the prepared train split for planning retrieval.")
    parser.add_argument("--normalize_triggers", action="store_true", help="Apply dataset-specific trigger span normalization before formatting predictions.")
    parser.add_argument("--doc_argument_dedup", action="store_true", help="Deduplicate repeated argument spans at document level for the same event type and role before formatting predictions.")
    parser.add_argument("--planning_profile", default="generic", choices=["auto", "generic", "casie", "casie_strict_trigger", "mapcoder", "genia"])
    parser.add_argument("--domain_adapter", default=None, choices=["none", "genia"], help="Deprecated alias that sets both trigger_adapter and output_adapter when provided.")
    parser.add_argument("--trigger_adapter", default="none", choices=["none", "genia"], help="Optional trigger-side/domain-specific planner adapter.")
    parser.add_argument("--output_adapter", default="none", choices=["none", "genia"], help="Optional output-side/domain-specific post-processing adapter.")
    parser.add_argument("--planning_backend", default="aec", choices=["aec", "dicore"], help="Planning backend to use for LLM planning.")
    parser.add_argument("--max_hypotheses", type=int, default=3, help="Maximum trigger hypotheses to keep per schema. Increase this for DiCoRe-style high-recall planning.")
    parser.add_argument("--max_patches", type=int, default=2, help="Maximum trigger/argument repair attempts per hypothesis.")
    parser.add_argument("--repair_mode", default="full", choices=["full", "light", "none"], help="Repair strategy: full keeps argument and trigger repair, light keeps only higher-value trigger-level retries, none disables hypothesis-level retries.")
    parser.add_argument("--mention_first_coding", action="store_true", help="Use mention-first, arguments-second LLM coding instead of generating full event objects in one step.")
    parser.add_argument("--argument_mode", default="free", choices=["free", "candidate_select", "hybrid", "hybrid_candidate"], help="Argument extraction mode. candidate_select constrains role fillers to generic candidate spans near the trigger; hybrid uses free extraction plus generic filtering; hybrid_candidate uses hybrid extraction and fills empty roles through candidate selection.")
    parser.add_argument("--sample_mode", default="prepared", choices=["prepared", "raw_e2e"], help="Use schema-conditioned prepared prompts or raw window-level E2E samples.")
    parser.add_argument("--compact_output", action="store_true", help="Write a smaller results JSON by omitting bulky prompt/trace fields unless explicitly requested.")
    parser.add_argument("--save_prompt", action="store_true", help="Include the full prompt in each prediction record.")
    parser.add_argument("--save_trace", action="store_true", help="Include detailed pipeline trace data in each prediction record.")
    parser.add_argument("--save_prediction_run_summary", action="store_true", help="Include per-prediction run summaries inside each prediction record.")
    parser.add_argument("--save_sample_run_summaries", action="store_true", help="Include the top-level sample_run_summaries list in the output JSON.")
    parser.add_argument("--raw_e2e_schema_mode", default="all", choices=["all", "gold"], help="For raw_e2e, run all schemas or only gold schemas for analysis.")
    parser.add_argument("--llm_model", default=os.getenv("AEC_LLM_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o")
    parser.add_argument("--llm_base_url", default=os.getenv("AEC_LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    prepared_dir = Path(args.prepared_dir)
    paper_eval_max_dev_test_samples: int | None = None
    if args.paper_eval:
        input_dir = ROOT_DIR / "datasets" / "paper_eval_splits"
        prepared_dir = Path(args.paper_eval_prepared_dir)
        if args.split in {"dev", "test"}:
            paper_eval_max_dev_test_samples = args.max_samples if args.max_samples is not None else None
        if args.max_samples == 200:
            args.max_samples = None
    schema_roles: Dict[str, List[str]] | None = None
    if args.sample_mode == "raw_e2e":
        samples, schema_roles = load_raw_e2e_samples(input_dir, args.dataset_name, args.split, args.max_samples)
    else:
        if not args.skip_prepare:
            ensure_prepared_dataset(
                args.dataset_name,
                input_dir,
                prepared_dir,
                args.split,
                max_dev_test_samples_override=paper_eval_max_dev_test_samples,
            )
        try:
            samples = load_samples(prepared_dir, args.dataset_name, args.split, args.max_samples)
        except FileNotFoundError:
            if args.paper_eval:
                args.sample_mode = "raw_e2e"
                samples, schema_roles = load_raw_e2e_samples(input_dir, args.dataset_name, args.split, args.max_samples)
            else:
                raise

    if args.llm_model:
        os.environ["AEC_LLM_MODEL"] = args.llm_model
    if args.llm_base_url:
        os.environ["AEC_LLM_BASE_URL"] = args.llm_base_url

    save_prompt = args.save_prompt or not args.compact_output
    save_trace = args.save_trace or not args.compact_output
    save_prediction_run_summary = args.save_prediction_run_summary or not args.compact_output
    save_sample_run_summaries = args.save_sample_run_summaries or not args.compact_output

    example_db = build_example_db(prepared_dir, args.dataset_name, split="train") if args.use_prepared_exemplars else None
    pipeline = AECPipeline(
        retrieval_agent=RetrievalAgent(example_db=example_db),
        max_hypotheses=args.max_hypotheses,
        max_patches=args.max_patches,
        repair_mode=args.repair_mode,
        planning_backend=args.planning_backend,
    )
    pipeline.coding_agent.use_mention_first_coding = args.mention_first_coding
    pipeline.coding_agent.argument_mode = args.argument_mode
    if args.planning_profile == "auto":
        if args.dataset_name == "casie":
            effective_planning_profile = "casie"
        elif args.dataset_name == "genia2011":
            effective_planning_profile = "genia"
        else:
            effective_planning_profile = "generic"
    else:
        effective_planning_profile = args.planning_profile
    effective_trigger_adapter = args.domain_adapter if args.domain_adapter is not None else args.trigger_adapter
    effective_output_adapter = args.domain_adapter if args.domain_adapter is not None else args.output_adapter
    pipeline.trigger_adapter = effective_trigger_adapter
    pipeline.output_adapter = effective_output_adapter
    pipeline.planning_agent.trigger_adapter = effective_trigger_adapter
    pipeline.coding_agent.output_adapter = effective_output_adapter
    pipeline.coding_agent.force_hypothesis_trigger_coding = (
        effective_planning_profile == "genia" and args.planning_backend == "dicore"
    )
    prediction_records = []
    run_summaries = []
    total_samples = len(samples)
    progress_enabled = not args.no_progress
    sample_iterator = tqdm(
        enumerate(samples, start=1),
        total=total_samples,
        desc=f"Running {args.dataset_name}/{args.split}",
        unit="sample",
        dynamic_ncols=True,
    ) if progress_enabled else enumerate(samples, start=1)
    aggregate_summary = {
        "samples": 0,
        "hypothesis_count": 0,
        "validated_event_count": 0,
        "verified_pass_count": 0,
        "verified_fail_count": 0,
        "repair_attempt_count": 0,
        "repair_changed_count": 0,
        "trigger_normalization_count": 0,
        "verifier_categories": {},
        "repair_routes": {},
        "repair_outcomes": {},
    }
    for sample_idx, sample in sample_iterator:
        if args.sample_mode == "raw_e2e":
            assert schema_roles is not None
            class_name = "ALL"
            role_names = []
            text = sample["input"]
        else:
            class_name, role_names, text = parse_prompt(sample["input"])
        if progress_enabled and hasattr(sample_iterator, "set_postfix"):
            sample_iterator.set_postfix(
                sample=f"{sample_idx}/{total_samples}",
                event=class_name,
                stage="start",
                hyp=aggregate_summary["hypothesis_count"],
                valid=aggregate_summary["validated_event_count"],
                fail=aggregate_summary["verified_fail_count"],
                norm=aggregate_summary["trigger_normalization_count"],
                refresh=True,
            )
        if args.sample_mode == "raw_e2e":
            assert schema_roles is not None
            prediction, trace, run_summary = build_raw_e2e_prediction(
                pipeline=pipeline,
                schema_roles=schema_roles,
                text=text,
                gold_output=sample["output"],
                use_llm_plan=args.use_llm_plan,
                use_llm_coding=args.use_llm_coding,
                dataset_name=args.dataset_name,
                planning_profile=effective_planning_profile,
                trigger_adapter=effective_trigger_adapter,
                output_adapter=effective_output_adapter,
                normalize_triggers=args.normalize_triggers,
                doc_argument_dedup=args.doc_argument_dedup,
                schema_mode=args.raw_e2e_schema_mode,
            )
        else:
            prediction, trace, run_summary = build_prediction(
                pipeline=pipeline,
                class_name=class_name,
                role_names=role_names,
                text=text,
                gold_output=sample["output"],
                use_llm_plan=args.use_llm_plan,
                use_llm_coding=args.use_llm_coding,
                dataset_name=args.dataset_name,
                planning_profile=effective_planning_profile,
                trigger_adapter=effective_trigger_adapter,
                output_adapter=effective_output_adapter,
                normalize_triggers=args.normalize_triggers,
                doc_argument_dedup=args.doc_argument_dedup,
            )
        scorer_input = text
        if args.sample_mode == "raw_e2e":
            scorer_input = text
        elif DATASET_TO_TASK[args.dataset_name] == "ed":
            scorer_input = f"# task header\n\n# task schema\n\n{sample['input']}"
        run_summaries.append(run_summary)
        aggregate_summary["samples"] += 1
        for key in ["hypothesis_count", "validated_event_count", "verified_pass_count", "verified_fail_count", "repair_attempt_count", "repair_changed_count", "trigger_normalization_count"]:
            aggregate_summary[key] += int(run_summary.get(key, 0))
        for bucket_name in ["verifier_categories", "repair_routes", "repair_outcomes"]:
            bucket = run_summary.get(bucket_name, {})
            if isinstance(bucket, dict):
                for name, value in bucket.items():
                    aggregate_summary[bucket_name][name] = aggregate_summary[bucket_name].get(name, 0) + int(value)
        record = {
            "Input": scorer_input,
            "Label": sample["output"],
            "Prediction": prediction,
        }
        if save_prompt:
            record["Prompt"] = build_raw_e2e_prompt(text, schema_roles) if args.sample_mode == "raw_e2e" and schema_roles is not None else sample.get("input", scorer_input)
        if save_trace:
            record["Trace"] = trace
        if save_prediction_run_summary:
            record["RunSummary"] = run_summary
        prediction_records.append(record)
        if progress_enabled and hasattr(sample_iterator, "set_postfix"):
            processed = max(aggregate_summary["samples"], 1)
            sample_iterator.set_postfix(
                sample=f"{sample_idx}/{total_samples}",
                event=class_name,
                stage="done",
                hyp=aggregate_summary["hypothesis_count"],
                valid=aggregate_summary["validated_event_count"],
                fail=aggregate_summary["verified_fail_count"],
                norm=aggregate_summary["trigger_normalization_count"],
                avg_valid=f"{aggregate_summary['validated_event_count'] / processed:.2f}",
                refresh=True,
            )

    metrics = evaluate_predictions(args.dataset_name, prediction_records)
    trigger_agnostic_metrics = compute_trigger_agnostic_argument_metrics(prediction_records)
    primary_metrics = build_primary_metrics(metrics, trigger_agnostic_metrics)
    derived_analytics = build_derived_analytics(aggregate_summary)
    dominant_summary = build_dominant_summary(aggregate_summary)

    output_file = Path(args.output_file) if args.output_file else ROOT_DIR / "demo_result" / f"{args.dataset_name}_{args.split}_predictions.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_payload = {
        "dataset": args.dataset_name,
        "split": args.split,
        "paper_eval": args.paper_eval,
        "input_dir": str(input_dir),
        "prepared_dir": str(prepared_dir),
        "sample_mode": args.sample_mode,
        "raw_e2e_schema_mode": args.raw_e2e_schema_mode if args.sample_mode == "raw_e2e" else None,
        "planning_profile": effective_planning_profile,
        "requested_planning_profile": args.planning_profile,
        "trigger_adapter": effective_trigger_adapter,
        "output_adapter": effective_output_adapter,
        "domain_adapter": args.domain_adapter,
        "normalize_triggers": args.normalize_triggers,
        "num_samples": len(prediction_records),
        "metrics": primary_metrics,
        "primary_metrics": primary_metrics,
        "run_summary": aggregate_summary,
        "derived_analytics": derived_analytics,
        "dominant_summary": dominant_summary,
        "output_options": {
            "compact_output": args.compact_output,
            "save_prompt": save_prompt,
            "save_trace": save_trace,
            "save_prediction_run_summary": save_prediction_run_summary,
            "save_sample_run_summaries": save_sample_run_summaries,
            "mention_first_coding": args.mention_first_coding,
            "argument_mode": args.argument_mode,
            "repair_mode": args.repair_mode,
            "doc_argument_dedup": args.doc_argument_dedup,
        },
        "predictions": prediction_records,
    }
    if save_sample_run_summaries:
        output_payload["sample_run_summaries"] = run_summaries

    with output_file.open("w", encoding="utf-8") as fh:
        json.dump(output_payload, fh, indent=2)

    light_output_file = output_file.with_name(f"{output_file.stem}.light{output_file.suffix}")
    light_prediction_records = [
        {
            "Input": record.get("Input", ""),
            "Label": record.get("Label", ""),
            "Prediction": record.get("Prediction", ""),
            "RunSummary": record.get("RunSummary", {}),
        }
        for record in prediction_records
    ]
    light_payload = {
        "dataset": output_payload["dataset"],
        "split": output_payload["split"],
        "paper_eval": output_payload["paper_eval"],
        "sample_mode": output_payload["sample_mode"],
        "planning_profile": output_payload["planning_profile"],
        "requested_planning_profile": output_payload["requested_planning_profile"],
        "trigger_adapter": output_payload["trigger_adapter"],
        "output_adapter": output_payload["output_adapter"],
        "domain_adapter": output_payload["domain_adapter"],
        "normalize_triggers": output_payload["normalize_triggers"],
        "num_samples": output_payload["num_samples"],
        "metrics": primary_metrics,
        "primary_metrics": primary_metrics,
        "run_summary": aggregate_summary,
        "derived_analytics": derived_analytics,
        "dominant_summary": dominant_summary,
        "output_options": {
            **output_payload["output_options"],
            "light_output": True,
            "omitted_fields": ["Trace", "Prompt"],
        },
        "predictions": light_prediction_records,
    }
    with light_output_file.open("w", encoding="utf-8") as fh:
        json.dump(light_payload, fh, indent=2)

    print(f"Saved predictions to: {output_file}")
    print(f"Saved light predictions to: {light_output_file}")
    print("Primary metrics:")
    print(json.dumps(primary_metrics, indent=2))
    print("Run summary:")
    print(
        json.dumps(
            {
                "samples": aggregate_summary["samples"],
                "hypothesis_count": aggregate_summary["hypothesis_count"],
                "validated_event_count": aggregate_summary["validated_event_count"],
                "verified_pass_count": aggregate_summary["verified_pass_count"],
                "verified_fail_count": aggregate_summary["verified_fail_count"],
                "repair_attempt_count": aggregate_summary["repair_attempt_count"],
                "repair_changed_count": aggregate_summary["repair_changed_count"],
                "trigger_normalization_count": aggregate_summary["trigger_normalization_count"],
                "verifier_categories": aggregate_summary["verifier_categories"],
                "repair_routes": aggregate_summary["repair_routes"],
                "repair_outcomes": aggregate_summary["repair_outcomes"],
            },
            indent=2,
        )
    )
    print("Derived analytics:")
    print(json.dumps(derived_analytics, indent=2))
    print("Dominant summary:")
    print(json.dumps(dominant_summary, indent=2))


if __name__ == "__main__":
    main()
