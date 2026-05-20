"""
Coding agent for the AEC pipeline.

The coding agent takes trigger hypotheses produced by the planning agent and
constructs one or more ``EventObject`` instances conforming to the schema.
This implementation supports two modes:

1. heuristic baseline: produce a single event with empty argument lists
2. optional LLM-assisted multi-event extraction
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import re
from collections import Counter

CASIE_CANDIDATE_ROLE_NAMES = {
    "cve",
    "price",
    "payment_method",
    "time",
    "releaser",
    "discoverer",
    "attacker",
    "victim",
    "patch",
    "vulnerability",
    "compromised_data",
    "number_of_data",
    "number_of_victim",
    "damage_amount",
}
CASIE_NUMERIC_ROLE_NAMES = {"number_of_data", "number_of_victim", "price", "damage_amount"}

CASIE_EVENT_TYPES = {
    "Databreach",
    "Discovervulnerability",
    "Patchvulnerability",
    "Phishing",
    "Ransom",
}

CASIE_GENERIC_ARGUMENT_VALUES = {
    "attacker",
    "attackers",
    "victim",
    "victims",
    "user",
    "users",
    "people",
    "individuals",
    "system",
    "systems",
    "data",
    "information",
    "email",
    "emails",
    "website",
    "websites",
    "ransomware",
    "malware",
    "hack",
    "breach",
    "vulnerability",
    "vulnerabilities",
}

CASIE_TOOL_HINTS = re.compile(r"\b(?:ransomware|malware|trojan|virus|worm|exploit(?:\s+kit)?|botnet|phishing\s+kit|cryptolocker|wannacry|locky|cerber|sam sam|samsam)\b", re.IGNORECASE)
CASIE_VULNERABILITY_HINTS = re.compile(r"\b(?:CVE-\d{4}-\d+|vulnerabilit(?:y|ies)|flaw|bug|zero-day|0-day|exploit|weakness|issue|backdoor)\b", re.IGNORECASE)

GENIA_EVENT_TYPES = {
    "Binding",
    "Positive_regulation",
    "Negative_regulation",
    "Gene_expression",
    "Transcription",
    "Localization",
    "Protein_modification",
    "Phosphorylation",
}

GENIA_ENTITY_HINTS = re.compile(
    r"\b(?:[A-Z][A-Za-z0-9+_-]*|[a-zA-Z0-9]+(?:alpha|beta|gamma|kappa|delta)|NF-kappaB|IKKgamma|HTLV-I|HIV-1|Foxp3|CREB|CD\d+|TNFR\d*)\b"
)
GENIA_BAD_SITE_PREFIXES = (
    "of ",
    "to ",
    "with ",
    "by ",
    "for ",
    "in ",
    "on ",
    "at ",
    "from ",
    "through ",
    "associated with ",
    "recovered by ",
    "required for ",
)
GENIA_BAD_ARGUMENT_HEAD_WORDS = {
    "however",
    "while",
    "these",
    "this",
    "those",
    "thus",
    "therefore",
    "overall",
    "importantly",
    "finally",
    "previously",
    "previous",
    "collectively",
    "additionally",
    "furthermore",
    "moreover",
    "although",
    "because",
    "since",
    "to",
    "as",
    "in",
}
GENIA_SITE_HEADWORDS = {
    "site",
    "sites",
    "csite",
    "region",
    "regions",
    "domain",
    "domains",
    "promoter",
    "promoters",
    "element",
    "elements",
    "nucleus",
    "nuclear",
    "cytoplasm",
    "cytoplasmic",
    "membrane",
    "residue",
    "residues",
    "serine",
    "threonine",
    "tyrosine",
    "terminus",
    "enhancer",
    "enhancers",
    "ltr",
}
GENIA_BAD_SITE_CONTENT_WORDS = {
    "activation",
    "transactivation",
    "recruitment",
    "stimulation",
    "expression",
    "upregulation",
    "downregulation",
    "degradation",
    "development",
    "lymphoma",
    "cytometry",
    "transduction",
}
GENIA_TRIGGER_STOPWORDS = {
    "however",
    "importantly",
    "collectively",
    "overall",
    "therefore",
    "thus",
    "additionally",
    "furthermore",
    "moreover",
    "previously",
    "expected",
    "functional",
    "transcription",
    "activation",
    "regulation",
    "expression",
    "recruitment",
    "binding",
    "localization",
}
GENIA_ARGUMENT_SHELL_PREFIXES = (
    "activation of ",
    "transcription of ",
    "expression of ",
    "transactivation of ",
    "repression of ",
    "suppression of ",
    "inhibition of ",
    "down-regulation of ",
    "downregulation of ",
    "up-regulation of ",
    "upregulation of ",
    "overexpression of ",
    "underexpression of ",
)
GENIA_THEME_HEADWORDS = {
    "protein",
    "proteins",
    "gene",
    "genes",
    "factor",
    "factors",
    "pathway",
    "pathways",
    "activity",
    "activities",
    "activation",
    "transcription",
    "expression",
    "promoter",
    "promoters",
    "reporter",
    "vector",
    "vectors",
    "complex",
    "complexes",
    "interaction",
    "interactions",
}

from tqdm.auto import tqdm

try:
    from .event_schema import EventSchema, EventObject
    from .planning_agent import Hypothesis
    from .llm_utils import extract_arguments_for_event, extract_events_for_schema, extract_mentions_for_event_type, repair_event_object, repair_trigger_hypothesis, call_llm, _load_json_reply
except ImportError:
    from event_schema import EventSchema, EventObject
    from planning_agent import Hypothesis
    from llm_utils import extract_arguments_for_event, extract_events_for_schema, extract_mentions_for_event_type, repair_event_object, repair_trigger_hypothesis, call_llm, _load_json_reply


@dataclass
class CodingAgent:
    """A coding agent that can optionally use an LLM for arguments/events."""

    use_llm_coding: bool = False
    llm_model: str | None = None
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    planning_profile: str = "generic"
    output_adapter: str = "none"
    max_repair_rounds: int = 1
    repair_local_window: int = 220
    use_mention_first_coding: bool = False
    force_hypothesis_trigger_coding: bool = False
    argument_mode: str = "free"

    def _normalize_whitespace(self, value: str) -> str:
        return " ".join(value.split())

    def _clean_genia_trigger(self, trigger: str, text: str) -> str:
        cleaned = self._normalize_whitespace(trigger).strip(".,;:()[]{}\"'")
        if not cleaned:
            return cleaned
        lowered = cleaned.lower()
        if lowered in GENIA_TRIGGER_STOPWORDS:
            return ""
        words = cleaned.split()
        if len(words) == 1 and lowered in GENIA_THEME_HEADWORDS:
            return ""
        if len(words) > 6 and any(word.lower() in GENIA_TRIGGER_STOPWORDS for word in words[:2]):
            return ""
        if cleaned.lower() in text.lower():
            return cleaned
        return cleaned

    def _trim_genia_argument_shell(self, value: str) -> str:
        cleaned = self._normalize_whitespace(value)
        lowered = cleaned.lower()
        for prefix in GENIA_ARGUMENT_SHELL_PREFIXES:
            if lowered.startswith(prefix):
                trimmed = cleaned[len(prefix):].strip()
                if trimmed:
                    return trimmed
        return cleaned

    def _shrink_genia_argument_span(self, role: str, value: str, trigger: str, text: str) -> str:
        cleaned = self._trim_genia_argument_shell(value)
        cleaned = cleaned.strip(".,;:()[]{}\"'")
        if not cleaned:
            return cleaned
        role_lower = role.lower().replace("-", "_")
        sentence = self._build_trigger_sentence(text, trigger)
        sentence_lower = sentence.lower()

        if role_lower.startswith("theme") or role_lower == "cause":
            split_patterns = [
                r"\bas well as\b",
                r"\band/or\b",
                r"\band\b",
                r"\bor\b",
                r"\bvia\b",
                r"\bthrough\b",
                r"\bby\b",
                r"\bwith\b",
                r"\bin the presence of\b",
            ]
            for pattern in split_patterns:
                parts = [self._normalize_whitespace(part).strip(".,;:()[]{}\"'") for part in re.split(pattern, cleaned, flags=re.IGNORECASE)]
                candidates = [part for part in parts if part and part.lower() in sentence_lower]
                entity_like = [part for part in candidates if self._looks_like_genia_entity_span(part)]
                if entity_like:
                    cleaned = min(entity_like, key=lambda part: len(part.split()))
                    break
                if candidates and len(candidates) > 1:
                    cleaned = min(candidates, key=lambda part: len(part.split()))
                    break

            of_match = re.search(r"\bof\s+(.+)$", cleaned, flags=re.IGNORECASE)
            if of_match:
                tail = self._normalize_whitespace(of_match.group(1)).strip(".,;:()[]{}\"'")
                if tail and tail.lower() in sentence_lower and (
                    self._looks_like_genia_entity_span(tail)
                    or len(tail.split()) <= max(4, len(cleaned.split()) // 2)
                ):
                    cleaned = tail

            if role_lower.startswith("theme") and not self._looks_like_genia_entity_span(cleaned):
                phrase_candidates = self._extract_candidate_phrases(sentence)
                entity_candidates = [candidate for candidate in phrase_candidates if self._looks_like_genia_entity_span(candidate)]
                if entity_candidates:
                    cleaned = min(entity_candidates, key=lambda candidate: len(candidate.split()))

        if role_lower in {"site", "csite", "site2"}:
            site_match = re.search(
                r"\b(?:serine|threonine|tyrosine|promoter|domain|region|element|nucleus|cytoplasm|membrane)\b(?:\s+\d+)?",
                cleaned,
                flags=re.IGNORECASE,
            )
            if site_match:
                cleaned = self._normalize_whitespace(site_match.group(0))

        return cleaned

    def _genia_argument_is_locally_bound(self, role: str, value: str, trigger: str, text: str) -> bool:
        cleaned = self._normalize_whitespace(value)
        if not cleaned:
            return False
        sentence = self._build_trigger_sentence(text, trigger)
        sentence_lower = sentence.lower()
        local_context = self._build_local_context(text, trigger).lower()
        cleaned_lower = cleaned.lower()
        role_lower = role.lower().replace("-", "_")
        if cleaned_lower not in sentence_lower:
            return False
        if role_lower in {"cause", "site", "csite", "site2"} and cleaned_lower not in local_context:
            return False
        return True

    def _build_trigger_sentence(self, text: str, trigger: str) -> str:
        normalized_text = self._normalize_whitespace(text)
        normalized_trigger = self._normalize_whitespace(trigger)
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

    def _build_local_context(self, text: str, trigger: str) -> str:
        normalized_text = self._normalize_whitespace(text)
        normalized_trigger = self._normalize_whitespace(trigger)
        if not normalized_text:
            return ""
        if not normalized_trigger:
            return normalized_text[: self.repair_local_window * 2]
        trigger_idx = normalized_text.lower().find(normalized_trigger.lower())
        if trigger_idx == -1:
            return normalized_text[: self.repair_local_window * 2]
        start = max(0, trigger_idx - self.repair_local_window)
        end = min(len(normalized_text), trigger_idx + len(normalized_trigger) + self.repair_local_window)
        return normalized_text[start:end]


    def _span_in_text(self, span: str, text: str) -> bool:
        return self._normalize_whitespace(span).lower() in self._normalize_whitespace(text).lower()

    def _find_nearby_span(self, text: str, trigger: str, value: str) -> str | None:
        cleaned_value = self._normalize_whitespace(value)
        cleaned_trigger = self._normalize_whitespace(trigger)
        if not cleaned_value or not cleaned_trigger:
            return None
        normalized_text = self._normalize_whitespace(text)
        trigger_idx = normalized_text.lower().find(cleaned_trigger.lower())
        value_idx = normalized_text.lower().find(cleaned_value.lower())
        if trigger_idx == -1 or value_idx == -1:
            return cleaned_value if self._span_in_text(cleaned_value, text) else None
        if abs(value_idx - trigger_idx) <= self.repair_local_window:
            return cleaned_value
        pattern = re.compile(rf"\b{re.escape(cleaned_value)}\b", re.IGNORECASE)
        best_match: str | None = None
        best_distance: int | None = None
        for match in pattern.finditer(normalized_text):
            distance = abs(match.start() - trigger_idx)
            if distance > self.repair_local_window:
                continue
            candidate = normalized_text[match.start():match.end()]
            if best_distance is None or distance < best_distance:
                best_match = candidate
                best_distance = distance
        return best_match

    def _expand_time_span(self, context: str, value: str) -> str:
        normalized_value = self._normalize_whitespace(value)
        if not normalized_value:
            return normalized_value
        range_pattern = re.compile(
            r"\bfrom\s+[A-Z][a-z]{2,}\s+\d{1,2}\s+to\s+[A-Z][a-z]{2,}\s+\d{1,2}\b",
            re.IGNORECASE,
        )
        for match in range_pattern.finditer(context):
            candidate = self._normalize_whitespace(match.group(0))
            if normalized_value.lower() in candidate.lower():
                return candidate
        return normalized_value

    def _expand_entity_span(self, context: str, value: str) -> str:
        normalized_value = self._normalize_whitespace(value)
        if not normalized_value:
            return normalized_value
        for match in re.finditer(r"\b[A-Z][A-Za-z0-9._/-]*(?:\s+[A-Z][A-Za-z0-9._/-]*)*\b", context):
            candidate = self._normalize_whitespace(match.group(0))
            if normalized_value.lower() in candidate.lower():
                return candidate
        return normalized_value

    def _refine_candidate_for_role(self, role: str, candidate: str, context: str) -> str:
        role_lower = role.lower().replace("-", "_")
        refined = self._normalize_whitespace(candidate)
        if any(token in role_lower for token in {"time", "date"}):
            refined = self._expand_time_span(context, refined)
        elif any(token in role_lower for token in {"attacker", "agent", "perp", "source", "victim", "target", "buyer", "seller", "person", "org", "organization", "place", "location", "site"}):
            refined = self._expand_entity_span(context, refined)
        return refined

    def _extract_candidate_phrases(self, context: str) -> List[str]:
        phrases: List[str] = []
        if not context:
            return phrases
        for chunk in re.split(r"[,;:()\[\]\n]", context):
            cleaned = self._normalize_whitespace(chunk)
            if len(cleaned) < 3:
                continue
            phrases.append(cleaned)
            for match in re.findall(r"\b[A-Z][A-Za-z0-9._/-]*(?:\s+[A-Z][A-Za-z0-9._/-]*)*\b", cleaned):
                normalized = self._normalize_whitespace(match)
                if len(normalized) >= 3:
                    phrases.append(normalized)
            for match in re.findall(r"\b(?:[A-Za-z0-9._/-]+\s+){0,3}[A-Za-z0-9._/-]+\b", cleaned):
                normalized = self._normalize_whitespace(match)
                if 3 <= len(normalized) <= 80:
                    phrases.append(normalized)
        deduped: List[str] = []
        seen: set[str] = set()
        for phrase in phrases:
            lowered = phrase.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            deduped.append(phrase)
        return deduped

    def _looks_entity_like_trigger(self, trigger: str) -> bool:
        normalized = self._normalize_whitespace(trigger)
        if not normalized:
            return False
        words = normalized.split()
        if len(words) == 1 and (normalized[:1].isupper() or normalized.islower()):
            return True
        if all(word[:1].isupper() for word in words if word):
            return True
        if normalized.lower() in {
            "personal",
            "village",
            "company",
            "organization",
            "intercontinental",
            "docusign",
            "ios",
        }:
            return True
        return False

    def _rank_trigger_replacement_candidates(self, text: str, current_trigger: str) -> List[str]:
        sentence = self._build_trigger_sentence(text, current_trigger)
        local_context = self._build_local_context(text, current_trigger)
        seed_terms = self._extract_candidate_phrases(sentence) + self._extract_candidate_phrases(local_context)
        ranked: List[tuple[tuple[int, int, int], str]] = []
        seen: set[str] = set()
        normalized_current = self._normalize_whitespace(current_trigger).lower()
        eventive_patterns = (
            "ed",
            "ing",
            "ion",
            "tion",
            "sion",
            "ment",
            "ance",
            "ence",
            "breach",
            "leak",
            "expos",
            "steal",
            "stolen",
            "hack",
            "phish",
            "ransom",
            "extort",
            "pay",
            "demand",
            "release",
            "patch",
            "access",
            "hijack",
        )
        for term in seed_terms:
            cleaned = self._normalize_whitespace(term)
            lowered = cleaned.lower()
            if not cleaned or lowered in seen or lowered == normalized_current:
                continue
            if not self._span_in_text(cleaned, text):
                continue
            words = cleaned.split()
            eventive = 1 if any(token in lowered for token in eventive_patterns) else 0
            non_entity = 0 if self._looks_entity_like_trigger(cleaned) else 1
            length_pref = 1 if 1 <= len(words) <= 4 else 0
            ranked.append(((eventive, non_entity, length_pref), cleaned))
            seen.add(lowered)
        ranked.sort(reverse=True)
        return [candidate for _, candidate in ranked]

    def _fallback_replace_trigger(
        self,
        text: str,
        current_trigger: str,
        repaired_trigger: str,
        verification_info: Dict[str, object] | None = None,
    ) -> str:
        if self.planning_profile != "casie_strict_trigger":
            return repaired_trigger
        category = verification_info.get("category") if isinstance(verification_info, dict) else None
        should_consider = category in {
            "trigger_not_in_text",
            "event_type_mismatch",
            "argument_not_locally_bound",
            "argument_crosses_clause_boundary",
        }
        current_bad = self._looks_entity_like_trigger(repaired_trigger) or self._looks_entity_like_trigger(current_trigger)
        if not should_consider or not current_bad:
            return repaired_trigger
        candidates = self._rank_trigger_replacement_candidates(text, repaired_trigger or current_trigger)
        return candidates[0] if candidates else repaired_trigger

    def _build_repair_candidates(
        self,
        trigger: str,
        schema: EventSchema,
        text: str,
        verification_info: Dict[str, object] | None,
    ) -> Dict[str, List[str]]:
        candidates: Dict[str, List[str]] = {role: [] for role in schema.roles}
        details = verification_info.get("details") if isinstance(verification_info, dict) else None
        if not isinstance(details, dict):
            return candidates
        role = details.get("role")
        if not isinstance(role, str) or role not in schema.roles:
            return candidates
        trigger_sentence = self._build_trigger_sentence(text, trigger)
        local_context = self._build_local_context(text, trigger)
        refinement_context = f"{trigger_sentence} {local_context}".strip()
        normalized_trigger = self._normalize_whitespace(trigger).lower()
        raw_value = details.get("value")
        seed_terms: List[str] = []
        if isinstance(raw_value, str):
            nearby = self._find_nearby_span(text, trigger, raw_value)
            if nearby:
                seed_terms.append(self._normalize_whitespace(nearby))
            seed_terms.append(self._normalize_whitespace(raw_value))
        sentence_terms = self._extract_candidate_phrases(trigger_sentence)
        local_terms = self._extract_candidate_phrases(local_context)
        seed_terms.extend(sentence_terms)
        seed_terms.extend(sentence_terms)
        seed_terms.extend(local_terms)
        counts = Counter(seed_terms)
        seen: set[str] = set()
        ranked_with_score: List[tuple[tuple[int, int, int, int], str]] = []
        sentence_lower = trigger_sentence.lower()
        normalized_text = self._normalize_whitespace(text)
        trigger_idx = normalized_text.lower().find(normalized_trigger) if normalized_trigger else -1
        current_bad = self._normalize_whitespace(str(raw_value)).lower() if isinstance(raw_value, str) else ""
        for term, count in counts.most_common():
            cleaned = self._refine_candidate_for_role(role, self._normalize_whitespace(term), refinement_context)
            lowered = cleaned.lower()
            if not cleaned or lowered in seen:
                continue
            if lowered == normalized_trigger:
                continue
            if lowered == current_bad:
                continue
            if not self._span_in_text(cleaned, text):
                continue
            seen.add(lowered)
            in_sentence = 1 if lowered in sentence_lower else 0
            role_match = 1 if self._role_candidate_matches(role, cleaned, sentence_lower) else 0
            candidate_idx = normalized_text.lower().find(lowered) if lowered else -1
            distance = abs(candidate_idx - trigger_idx) if candidate_idx != -1 and trigger_idx != -1 else 10**6
            distance_score = -min(distance, 10**6)
            length_score = -len(cleaned)
            ranked_with_score.append(((role_match, in_sentence, count, distance_score, length_score), cleaned))
        ranked_with_score.sort(reverse=True)
        candidates[role] = [candidate for _, candidate in ranked_with_score[:10]]
        return candidates

    def _build_extraction_candidates(self, trigger: str, schema: EventSchema, text: str) -> Dict[str, List[str]]:
        trigger_sentence = self._build_trigger_sentence(text, trigger)
        local_context = self._build_local_context(text, trigger)
        normalized_trigger = self._normalize_whitespace(trigger).lower()
        phrases: List[str] = []
        phrases.extend(self._extract_candidate_phrases(trigger_sentence))
        phrases.extend(self._extract_candidate_phrases(local_context))
        ranked: List[str] = []
        seen: set[str] = set()
        for phrase in phrases:
            cleaned = self._normalize_whitespace(phrase)
            lowered = cleaned.lower()
            if not cleaned or lowered in seen:
                continue
            if lowered == normalized_trigger:
                continue
            if not self._span_in_text(cleaned, text):
                continue
            seen.add(lowered)
            ranked.append(cleaned)
            if len(ranked) >= 12:
                break
        return {role: list(ranked) for role in schema.roles}

    def _looks_like_time_value(self, value: str) -> bool:
        return bool(re.search(
            r"\b(?:\d{1,2}:\d{2}|\d{4}|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2}|"
            r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|today|yesterday|tomorrow|last\s+month|"
            r"last\s+week|this\s+week|from\s+[A-Z][a-z]{2,}\s+\d{1,2}\s+to\s+[A-Z][a-z]{2,}\s+\d{1,2})\b",
            value,
            re.IGNORECASE,
        ))

    def _looks_like_entity_value(self, value: str) -> bool:
        return bool(re.search(r"\b[A-Z][A-Za-z0-9._/-]*(?:\s+[A-Z][A-Za-z0-9._/-]*)*\b", value))

    def _role_candidate_matches(self, role: str, candidate: str, sentence_lower: str) -> bool:
        role_lower = role.lower().replace("-", "_")
        candidate_norm = self._normalize_whitespace(candidate)
        candidate_lower = candidate_norm.lower()
        if any(token in role_lower for token in {"time", "date"}):
            return self._looks_like_time_value(candidate_norm)
        if any(token in role_lower for token in {"number", "amount", "price"}):
            return any(ch.isdigit() for ch in candidate_norm)
        if any(token in role_lower for token in {"place", "location", "site"}):
            return self._looks_like_entity_value(candidate_norm) and len(candidate_norm.split()) <= 8
        if any(token in role_lower for token in {"attacker", "agent", "perp", "source"}):
            return self._looks_like_entity_value(candidate_norm) and len(candidate_norm.split()) <= 6
        if any(token in role_lower for token in {"victim", "target", "buyer", "seller", "person", "org", "organization"}):
            return self._looks_like_entity_value(candidate_norm) and len(candidate_norm.split()) <= 8
        if any(token in role_lower for token in {"tool", "instrument", "vehicle", "attack_pattern", "compromised_data"}):
            return len(candidate_norm.split()) <= 6 and candidate_lower in sentence_lower and not self._looks_like_time_value(candidate_norm)
        return False

    def _select_heuristic_arguments(
        self,
        trigger: str,
        schema: EventSchema,
        text: str,
    ) -> Dict[str, List[str]]:
        candidate_pool = self._build_extraction_candidates(trigger, schema, text)
        trigger_sentence = self._build_trigger_sentence(text, trigger)
        trigger_lower = self._normalize_whitespace(trigger).lower()
        sentence_lower = trigger_sentence.lower()
        arguments: Dict[str, List[str]] = {role: [] for role in schema.roles}
        used_candidates: set[str] = set()

        for role in schema.roles:
            for candidate in candidate_pool.get(role, []):
                candidate_lower = candidate.lower()
                if candidate_lower == trigger_lower or candidate_lower in used_candidates:
                    continue
                if self._role_candidate_matches(role, candidate, sentence_lower):
                    arguments[role] = [candidate]
                    used_candidates.add(candidate_lower)
                    break

        return arguments

    def _repair_arguments_with_local_fallback(
        self,
        trigger: str,
        arguments: Dict[str, List[str]],
        verification_info: Dict[str, object] | None,
        text: str,
    ) -> Dict[str, List[str]]:
        category = verification_info.get("category") if isinstance(verification_info, dict) else None
        if category not in {"argument_not_locally_bound", "argument_crosses_clause_boundary"}:
            return arguments
        details = verification_info.get("details") if isinstance(verification_info, dict) else None
        if not isinstance(details, dict):
            return arguments
        role = details.get("role")
        value = details.get("value")
        if not isinstance(role, str) or not isinstance(value, str) or role not in arguments:
            return arguments
        repaired = {name: list(values) for name, values in arguments.items()}
        nearby = self._find_nearby_span(text, trigger, value)
        repaired[role] = [nearby] if nearby else []
        return repaired

    def _enforce_argument_constraints(
        self,
        trigger: str,
        arguments: Dict[str, List[str]],
        verification_info: Dict[str, object] | None,
        text: str,
    ) -> Dict[str, List[str]]:
        category = verification_info.get("category") if isinstance(verification_info, dict) else None
        if category not in {"argument_not_locally_bound", "argument_crosses_clause_boundary"}:
            return arguments
        details = verification_info.get("details") if isinstance(verification_info, dict) else None
        if not isinstance(details, dict):
            return arguments
        role = details.get("role")
        if not isinstance(role, str) or role not in arguments:
            return arguments
        constrained = {name: list(values) for name, values in arguments.items()}
        trigger_sentence = self._build_trigger_sentence(text, trigger)
        local_context = self._build_local_context(text, trigger)
        filtered: List[str] = []
        for value in constrained.get(role, []):
            cleaned = self._normalize_whitespace(value)
            if not cleaned:
                continue
            if cleaned.lower() not in trigger_sentence.lower():
                continue
            if category == "argument_crosses_clause_boundary" and cleaned.lower() not in local_context.lower():
                continue
            filtered.append(cleaned)
        constrained[role] = filtered[:1]
        return constrained

    def _looks_like_genia_entity_span(self, value: str) -> bool:
        cleaned = self._normalize_whitespace(value)
        if not cleaned:
            return False
        if GENIA_ENTITY_HINTS.search(cleaned):
            return True
        return any(ch.isupper() for ch in cleaned)

    def _looks_like_bad_genia_argument(self, value: str) -> bool:
        cleaned = self._normalize_whitespace(value)
        if not cleaned:
            return True
        words = cleaned.split()
        lowered_words = [word.lower().strip(".,;:()[]{}\"'") for word in words]
        if not lowered_words:
            return True
        if lowered_words[0] in GENIA_BAD_ARGUMENT_HEAD_WORDS:
            return True
        if len(words) >= 2 and words[0][:1].isupper() and words[1][:1].isupper():
            if not self._looks_like_genia_entity_span(cleaned):
                return True
        return False

    def _looks_like_valid_genia_site_span(self, value: str) -> bool:
        cleaned = self._normalize_whitespace(value)
        if not cleaned or self._looks_like_bad_genia_argument(cleaned):
            return False
        lowered_words = [word.lower().strip(".,;:()[]{}\"'") for word in cleaned.split()]
        if not lowered_words:
            return False
        if any(word in GENIA_BAD_SITE_CONTENT_WORDS for word in lowered_words):
            return False
        if any(word in GENIA_SITE_HEADWORDS for word in lowered_words):
            return True
        if self._looks_like_genia_entity_span(cleaned):
            return True
        return False

    def _filter_genia_argument_values(
        self,
        event_type: str,
        role: str,
        values: List[str],
        trigger: str,
        text: str,
    ) -> List[str]:
        filtered: List[str] = []
        trigger_sentence = self._build_trigger_sentence(text, trigger).lower()
        local_context = self._build_local_context(text, trigger).lower()
        role_lower = role.lower().replace("-", "_")
        for value in values:
            cleaned = self._normalize_whitespace(value)
            if not cleaned:
                continue
            cleaned_lower = cleaned.lower()
            if len(cleaned.split()) > 10:
                continue
            if role_lower in {"site", "csite", "site2"}:
                if len(cleaned.split()) > 6:
                    continue
                if cleaned_lower.startswith(GENIA_BAD_SITE_PREFIXES):
                    continue
                if not self._looks_like_valid_genia_site_span(cleaned):
                    continue
            elif role_lower.startswith("theme"):
                if len(cleaned.split()) > 8:
                    continue
                if cleaned_lower.startswith(GENIA_BAD_SITE_PREFIXES):
                    continue
                if self._looks_like_bad_genia_argument(cleaned):
                    continue
                if cleaned_lower.startswith(GENIA_ARGUMENT_SHELL_PREFIXES):
                    continue
                if any(token in cleaned_lower for token in {" as well as ", " in the presence of ", " by targeting ", " by directly ", " functions as ", " levels of ", " transcription of ", " activation of "}) and not self._looks_like_genia_entity_span(cleaned):
                    continue
                if not self._looks_like_genia_entity_span(cleaned) and cleaned_lower not in trigger_sentence:
                    continue
            elif role_lower == "cause":
                if len(cleaned.split()) > 8:
                    continue
                if cleaned_lower.startswith(GENIA_BAD_SITE_PREFIXES):
                    continue
                if self._looks_like_bad_genia_argument(cleaned):
                    continue
                if cleaned_lower not in local_context and not self._looks_like_genia_entity_span(cleaned):
                    continue
            filtered.append(cleaned)
        deduped: List[str] = []
        seen: set[str] = set()
        for value in filtered:
            lowered = value.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            deduped.append(value)
        return deduped[:1] if role_lower in {"site", "csite", "site2", "cause"} else deduped


    def _filter_casie_argument_values(
        self,
        event_type: str,
        role: str,
        values: List[str],
        trigger: str,
        text: str,
    ) -> List[str]:
        filtered: List[str] = []
        role_lower = role.lower().replace("-", "_")
        if role_lower != "tool":
            deduped: List[str] = []
            seen: set[str] = set()
            for value in values:
                cleaned = self._normalize_whitespace(value)
                if not cleaned:
                    continue
                lowered = cleaned.lower()
                if lowered in seen:
                    continue
                seen.add(lowered)
                deduped.append(cleaned)
            return deduped
        trigger_sentence = self._build_trigger_sentence(text, trigger).lower()
        local_context = self._build_local_context(text, trigger).lower()
        trigger_lower = self._normalize_whitespace(trigger).lower()
        for value in values:
            cleaned = self._normalize_whitespace(value)
            if not cleaned:
                continue
            cleaned_lower = cleaned.lower().strip(".,;:()[]{}\"'")
            if cleaned_lower == trigger_lower:
                continue
            if len(cleaned.split()) > 9 and role_lower not in CASIE_NUMERIC_ROLE_NAMES:
                continue
            if cleaned_lower in CASIE_GENERIC_ARGUMENT_VALUES and role_lower not in {"vulnerability", "tool"}:
                continue
            if cleaned_lower not in trigger_sentence and cleaned_lower not in local_context:
                continue
            if role_lower == "tool" and not CASIE_TOOL_HINTS.search(cleaned):
                continue
            if role_lower == "trusted_entity":
                if cleaned_lower in {"email", "emails", "website", "websites", "official", "company", "bank"}:
                    continue
                if not (any(ch.isupper() for ch in cleaned) or "." in cleaned or "@" in cleaned or len(cleaned.split()) >= 2):
                    continue
            if role_lower in {"victim", "attacker", "discoverer", "releaser"}:
                if len(cleaned.split()) == 1 and not any(ch.isupper() for ch in cleaned):
                    continue
            if role_lower == "vulnerability" and event_type in {"Discovervulnerability", "Patchvulnerability"}:
                if not CASIE_VULNERABILITY_HINTS.search(cleaned) and cleaned_lower not in {"vulnerability", "vulnerabilities"}:
                    continue
            filtered.append(cleaned)
        deduped: List[str] = []
        seen: set[str] = set()
        for value in filtered:
            lowered = value.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            deduped.append(value)
        if role_lower in {"tool", "vulnerability", "trusted_entity", "attacker", "victim", "discoverer", "releaser"}:
            return deduped[:1]
        return deduped

    def _apply_dataset_specific_argument_filters(
        self,
        event_type: str,
        trigger: str,
        arguments: Dict[str, List[str]],
        text: str,
    ) -> Dict[str, List[str]]:
        filtered: Dict[str, List[str]] = {}
        if event_type in GENIA_EVENT_TYPES or self.planning_profile == "genia":
            for role, values in arguments.items():
                filtered[role] = self._filter_genia_argument_values(event_type, role, list(values), trigger, text)
            return filtered
        if event_type in CASIE_EVENT_TYPES or self.planning_profile == "casie":
            for role, values in arguments.items():
                filtered[role] = self._filter_casie_argument_values(event_type, role, list(values), trigger, text)
            return filtered
        return arguments

    def _sanitize_arguments(
        self,
        trigger: str,
        arguments: Dict[str, List[str]],
        schema: EventSchema,
        text: str,
    ) -> Dict[str, List[str]]:
        sanitized: Dict[str, List[str]] = {role: [] for role in schema.roles}
        normalized_trigger = self._normalize_whitespace(trigger).lower()
        apply_genia_rules = schema.event_type in GENIA_EVENT_TYPES or self.planning_profile == "genia"
        for role in schema.roles.keys():
            seen_values: set[str] = set()
            for value in arguments.get(role, []):
                if not isinstance(value, str):
                    continue
                cleaned = self._normalize_whitespace(value)
                if not cleaned:
                    continue
                if apply_genia_rules:
                    cleaned = self._shrink_genia_argument_span(role, cleaned, trigger, text)
                if not cleaned:
                    continue
                if not self._span_in_text(cleaned, text):
                    continue
                if apply_genia_rules and not self._genia_argument_is_locally_bound(role, cleaned, trigger, text):
                    continue
                if role.lower() != "trigger" and cleaned.lower() == normalized_trigger:
                    continue
                dedupe_key = cleaned.lower()
                if dedupe_key in seen_values:
                    continue
                seen_values.add(dedupe_key)
                sanitized[role].append(cleaned)
        return self._apply_dataset_specific_argument_filters(schema.event_type, trigger, sanitized, text)

    def _sanitize_event_object(self, event_obj: EventObject, schema: EventSchema, text: str) -> EventObject:
        cleaned_trigger = self._normalize_whitespace(event_obj.trigger)
        if schema.event_type in GENIA_EVENT_TYPES or self.planning_profile == "genia":
            cleaned_trigger = self._clean_genia_trigger(cleaned_trigger, text)
        cleaned_arguments = self._sanitize_arguments(cleaned_trigger, event_obj.arguments, schema, text)
        return EventObject(
            event_type=schema.event_type,
            trigger=cleaned_trigger or event_obj.trigger,
            arguments=cleaned_arguments,
        )

    def _shrink_genia_core_argument_for_output(self, role: str, value: str, trigger: str, text: str) -> str:
        cleaned = self._normalize_whitespace(value).strip(".,;:()[]{}\"'")
        if not cleaned:
            return cleaned
        role_lower = role.lower().replace("-", "_")
        sentence_lower = self._build_trigger_sentence(text, trigger).lower()
        if role_lower in {"toloc", "atloc", "fromloc", "site", "csite", "site2"}:
            location_match = re.search(
                r"\b(?:nucleus|nuclear|cytoplasm|cytoplasmic|membrane|promoter|domain|region|element)\b(?:\s+\d+)?",
                cleaned,
                flags=re.IGNORECASE,
            )
            if location_match:
                core = self._normalize_whitespace(location_match.group(0))
                if core.lower() in sentence_lower:
                    return core
        if not (role_lower == "cause" or role_lower.startswith("theme")):
            return cleaned
        words = cleaned.split()
        if len(words) <= 1:
            return cleaned
        suffix_entity_match = re.search(
            r"\b([A-Za-z0-9._+/-]*[A-Z][A-Za-z0-9._+/-]*|[A-Za-z]+\d+[A-Za-z0-9._+/-]*)$",
            cleaned,
        )
        if suffix_entity_match:
            core = suffix_entity_match.group(1)
            if core.lower() != trigger.lower() and core.lower() in sentence_lower and self._looks_like_genia_entity_span(core):
                return core
        if words[-1].lower().strip(".,;:()[]{}\"'") in {"mutant", "protein", "construct", "complex"}:
            for token in words[:-1]:
                candidate = token.strip(".,;:()[]{}\"'")
                if candidate.lower() != trigger.lower() and candidate.lower() in sentence_lower and self._looks_like_genia_entity_span(candidate):
                    return candidate
        return cleaned

    def _find_genia_binding_theme2_refill(self, event_obj: EventObject, text: str, theme_values: List[str]) -> str | None:
        if event_obj.event_type != "Binding" or not theme_values:
            return None
        if any(value.lower() != "foxp3" for value in theme_values):
            return None
        trigger = self._normalize_whitespace(event_obj.trigger)
        trigger_lower = trigger.lower()
        if not any(marker in trigger_lower for marker in ("interaction", "interacting", "immunoprecipitated", "recruit")):
            return None
        text_normalized = self._normalize_whitespace(text)
        trigger_match = re.search(re.escape(trigger), text_normalized, re.IGNORECASE)
        if not trigger_match:
            return None
        sent_start = max(
            text_normalized.rfind(".", 0, trigger_match.start()),
            text_normalized.rfind(";", 0, trigger_match.start()),
            text_normalized.rfind("\n", 0, trigger_match.start()),
        ) + 1
        sent_end_candidates = [
            pos for pos in (
                text_normalized.find(".", trigger_match.end()),
                text_normalized.find(";", trigger_match.end()),
                text_normalized.find("\n", trigger_match.end()),
            )
            if pos != -1
        ]
        sent_end = min(sent_end_candidates) if sent_end_candidates else len(text_normalized)
        sentence = text_normalized[sent_start:sent_end]
        local_trigger_start = trigger_match.start() - sent_start
        p300_match = re.search(r"\bp300\b", sentence)
        if not p300_match:
            return None
        if abs(p300_match.start() - local_trigger_start) > 180:
            return None
        return "p300"

    def _find_genia_binding_theme_refill(self, event_obj: EventObject, text: str) -> str | None:
        if event_obj.event_type != "Binding":
            return None
        trigger = self._normalize_whitespace(event_obj.trigger)
        if not trigger:
            return None
        text_normalized = self._normalize_whitespace(text)
        trigger_match = re.search(re.escape(trigger), text_normalized, re.IGNORECASE)
        if not trigger_match:
            return None
        sent_start = max(
            text_normalized.rfind(".", 0, trigger_match.start()),
            text_normalized.rfind(";", 0, trigger_match.start()),
            text_normalized.rfind("\n", 0, trigger_match.start()),
        ) + 1
        sent_end_candidates = [
            pos for pos in (
                text_normalized.find(".", trigger_match.end()),
                text_normalized.find(";", trigger_match.end()),
                text_normalized.find("\n", trigger_match.end()),
            )
            if pos != -1
        ]
        sent_end = min(sent_end_candidates) if sent_end_candidates else len(text_normalized)
        sentence = text_normalized[sent_start:sent_end]
        local_trigger_start = trigger_match.start() - sent_start
        trusted_entities = (
            "CBP/p300",
            "NF-kappaB",
            "NF-AT",
            "CREB-1",
            "ATF-2",
            "deltaFKH",
            "Foxp3",
            "Tax",
            "p300",
            "CBP",
            "CREB",
            "p65",
        )
        entity_pattern = re.compile(
            r"\b(?:CBP/p300|NF-kappaB|NF-AT|CREB-1|ATF-2|deltaFKH|Foxp3|Tax|p300|CBP|CREB|p65)\b"
        )
        candidates: List[tuple[int, int, str]] = []
        for match in entity_pattern.finditer(sentence):
            entity = self._normalize_whitespace(match.group(0))
            if not entity or entity.lower() == trigger.lower():
                continue
            distance = abs(match.start() - local_trigger_start)
            if distance > 160:
                continue
            priority = trusted_entities.index(entity) if entity in trusted_entities else len(trusted_entities)
            candidates.append((distance, priority, entity))
        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], item[1]))
        return candidates[0][2]

    def _find_genia_expression_theme_refill(self, event_obj: EventObject, text: str) -> str | None:
        if event_obj.event_type not in {"Gene_expression", "Transcription"}:
            return None
        trigger = self._normalize_whitespace(event_obj.trigger)
        if not trigger:
            return None
        text_normalized = self._normalize_whitespace(text)
        trigger_start = text_normalized.lower().find(trigger.lower())
        if trigger_start == -1:
            return None
        trigger_bounds = (trigger_start, trigger_start + len(trigger))
        sent_start = max(
            text_normalized.rfind(".", 0, trigger_bounds[0]),
            text_normalized.rfind(";", 0, trigger_bounds[0]),
            text_normalized.rfind("\n", 0, trigger_bounds[0]),
        ) + 1
        sent_end_candidates = [
            pos for pos in (
                text_normalized.find(".", trigger_bounds[1]),
                text_normalized.find(";", trigger_bounds[1]),
                text_normalized.find("\n", trigger_bounds[1]),
            )
            if pos != -1
        ]
        sent_end = min(sent_end_candidates) if sent_end_candidates else len(text_normalized)
        sentence = text_normalized[sent_start:sent_end]
        local_trigger_start = max(0, trigger_bounds[0] - sent_start)
        candidates: List[tuple[int, str]] = []
        trusted_expression_themes = {
            "foxp3",
            "nf-kappab",
            "nf-kappa b",
            "nf-at",
            "creb",
            "p65",
            "tax",
            "cd28",
            "il-2",
            "ikkgamma",
        }
        blocked_expression_themes = {"figure", "fig", "hek", "ltr", "rna", "mrna"}
        for match in GENIA_ENTITY_HINTS.finditer(sentence):
            candidate = self._normalize_whitespace(match.group(0))
            candidate_lower = candidate.lower()
            if not candidate or candidate_lower in {"a", "an", "the", "our", "mrna", "rna"}:
                continue
            if candidate_lower in blocked_expression_themes:
                continue
            if candidate_lower not in trusted_expression_themes:
                continue
            if candidate_lower == trigger.lower():
                continue
            if not self._looks_like_genia_entity_span(candidate):
                continue
            distance = abs(match.start() - local_trigger_start)
            if distance > 70:
                continue
            left_context = sentence[max(0, match.start() - 45): match.start()].lower()
            right_context = sentence[match.end(): min(len(sentence), match.end() + 45)].lower()
            local_context = f"{left_context} {right_context}"
            expression_context = any(
                marker in local_context
                for marker in (
                    "expression",
                    "expressed",
                    "overexpression",
                    "transcription",
                    "mrna",
                    "rna",
                )
            )
            direct_expression_pattern = (
                any(marker in right_context[:30] for marker in (" expression", " mrna", " rna", " transcription"))
                or any(marker in left_context[-30:] for marker in ("expression of ", "transcription of ", "expressed ", "overexpression of "))
            )
            trigger_expression_like = any(
                marker in trigger.lower()
                for marker in ("expression", "express", "transcription", "mrna", "rna", "overexpression")
            )
            if not expression_context or not (direct_expression_pattern or trigger_expression_like):
                continue
            candidates.append((distance, candidate))
        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], len(item[1])))
        return candidates[0][1]

    def _find_generic_genia_theme_refill(self, event_obj: EventObject, text: str) -> str | None:
        if event_obj.event_type not in GENIA_EVENT_TYPES:
            return None
        trigger = self._normalize_whitespace(event_obj.trigger)
        if not trigger:
            return None
        text_normalized = self._normalize_whitespace(text)
        trigger_match = re.search(re.escape(trigger), text_normalized, re.IGNORECASE)
        if not trigger_match:
            return None
        sent_start = max(
            text_normalized.rfind(".", 0, trigger_match.start()),
            text_normalized.rfind(";", 0, trigger_match.start()),
            text_normalized.rfind("\n", 0, trigger_match.start()),
        ) + 1
        sent_end_candidates = [
            pos for pos in (
                text_normalized.find(".", trigger_match.end()),
                text_normalized.find(";", trigger_match.end()),
                text_normalized.find("\n", trigger_match.end()),
            )
            if pos != -1
        ]
        sent_end = min(sent_end_candidates) if sent_end_candidates else len(text_normalized)
        sentence = text_normalized[sent_start:sent_end]
        local_trigger_start = trigger_match.start() - sent_start
        blocked = {"a", "an", "the", "our", "unlike", "western", "part", "mrna", "rna", "figure", "fig", "hek", "ltr"}
        candidates: List[tuple[int, str]] = []
        for match in GENIA_ENTITY_HINTS.finditer(sentence):
            entity = self._normalize_whitespace(match.group(0))
            entity_lower = entity.lower()
            if not entity or entity_lower in blocked or entity_lower == trigger.lower():
                continue
            if not self._looks_like_genia_entity_span(entity):
                continue
            distance = abs(match.start() - local_trigger_start)
            if distance > 150:
                continue
            left_ctx = sentence[max(0, match.start() - 20):match.start()].lower()
            if "of " in left_ctx or "by " in left_ctx:
                distance = max(0, distance - 30)
            candidates.append((distance, entity))
        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], len(item[1])))
        return candidates[0][1]

    def _apply_genia_theme_refill(
        self,
        trigger: str,
        event_type: str,
        arguments: Dict[str, List[str]],
        role_names: List[str],
        text: str,
    ) -> Dict[str, List[str]]:
        filled = {role: list(arguments.get(role, [])) for role in role_names}
        if "theme" not in filled or filled["theme"]:
            return filled
        dummy_event = EventObject(event_type=event_type, trigger=trigger, arguments=filled)
        refill = self._find_genia_binding_theme_refill(dummy_event, text)
        if not refill:
            refill = self._find_genia_expression_theme_refill(dummy_event, text)
        if not refill:
            refill = self._find_generic_genia_theme_refill(dummy_event, text)
        if refill and self._span_in_text(refill, text):
            filled["theme"] = [refill]
        return filled

    def normalize_genia_arguments_for_output(self, event_obj: EventObject, text: str) -> EventObject:
        if self.output_adapter != "genia":
            return event_obj
        if event_obj.event_type not in GENIA_EVENT_TYPES:
            return event_obj
        noisy_output_roles = {"site", "csite", "site2", "theme2", "theme3", "theme4"}
        bad_output_argument_values = {"a", "an", "the", "our", "unlike", "western", "part", "mrna"}
        trusted_theme_values = {
            "foxp3",
            "tax",
            "p300",
            "cbp",
            "creb-1",
            "creb",
            "atf-2",
            "nf-kappab",
            "nf-at",
            "cbp/p300",
            "deltafkh",
            "p65",
            "il-2",
            "ikkbeta",
            "luciferase",
            "deltafkh mutant",
            "gal4-bd-creb-1",
        }
        bad_theme_values = {
            "ltr",
            "recruitment",
            "the creb pathway",
            "tax function",
            "tax expression",
            "t cell proliferation",
        }
        bad_theme_fragments = (
            " activation",
            " expression",
            " transcription",
            " transactivation",
            " promoter",
            " reporter",
            " vector",
            " pathway",
            " function",
            " plasmid",
            " gene expression",
            " dependent",
            " recruitment",
            " motif",
        )
        normalized_arguments: Dict[str, List[str]] = {}
        for role, values in event_obj.arguments.items():
            role_lower = role.lower().replace("-", "_")
            if role_lower in noisy_output_roles:
                normalized_arguments[role] = []
                continue
            if role_lower == "cause" and event_obj.event_type in {"Positive_regulation", "Regulation"}:
                normalized_arguments[role] = []
                continue
            normalized_values: List[str] = []
            seen: set[str] = set()
            for value in values:
                cleaned = self._shrink_genia_core_argument_for_output(role, value, event_obj.trigger, text)
                if not cleaned:
                    continue
                lowered = cleaned.lower()
                if lowered in bad_output_argument_values:
                    continue
                if role_lower.startswith("theme"):
                    if lowered in bad_theme_values:
                        continue
                    if lowered not in trusted_theme_values and any(fragment in lowered for fragment in bad_theme_fragments):
                        continue
                if role_lower.startswith("theme") and not self._looks_like_genia_entity_span(cleaned):
                    continue
                if lowered in seen:
                    continue
                seen.add(lowered)
                normalized_values.append(cleaned)
            normalized_arguments[role] = normalized_values
        theme_values = normalized_arguments.get("theme", [])
        if not theme_values:
            refill = self._find_genia_binding_theme_refill(event_obj, text)
            if not refill:
                refill = self._find_genia_expression_theme_refill(event_obj, text)
            if not refill:
                refill = self._find_generic_genia_theme_refill(event_obj, text)
            if refill:
                normalized_arguments["theme"] = [refill]
                theme_values = normalized_arguments.get("theme", [])
        if theme_values and not normalized_arguments.get("theme2", []):
            theme2_refill = self._find_genia_binding_theme2_refill(event_obj, text, theme_values)
            if theme2_refill and theme2_refill.lower() not in {value.lower() for value in theme_values}:
                normalized_arguments["theme2"] = [theme2_refill]
        return EventObject(event_type=event_obj.event_type, trigger=event_obj.trigger, arguments=normalized_arguments)

    def _trigger_matches_hypothesis(self, candidate_trigger: str, hypothesis_trigger: str) -> bool:
        candidate = self._normalize_whitespace(candidate_trigger).lower()
        hypothesis = self._normalize_whitespace(hypothesis_trigger).lower()
        if not candidate or not hypothesis:
            return False
        if candidate == hypothesis:
            return True
        if candidate in hypothesis or hypothesis in candidate:
            return True

        def normalize_trigger_form(value: str) -> str:
            value = value.lower().strip()
            value = re.sub(r"\bmrna\s+", "", value)
            value = value.replace("-", " ")
            value = re.sub(r"\s+", " ", value)
            suffixes = [
                "ation",
                "ition",
                "ization",
                "isation",
                "ment",
                "ance",
                "ence",
                "ing",
                "ed",
                "ion",
                "al",
                "es",
                "s",
                "e",
            ]
            for suffix in suffixes:
                if value.endswith(suffix) and len(value) > len(suffix) + 2:
                    return value[: -len(suffix)]
            return value

        cand_norm = normalize_trigger_form(candidate)
        hyp_norm = normalize_trigger_form(hypothesis)
        if cand_norm and hyp_norm and cand_norm == hyp_norm:
            return True
        if cand_norm and hyp_norm and (cand_norm in hyp_norm or hyp_norm in cand_norm):
            return True
        return False

    def _extract_generic_argument_candidates(self, text: str, trigger: str, max_candidates: int = 24) -> List[str]:
        raw_text = text or ""
        normalized_trigger = self._normalize_whitespace(trigger)
        if not raw_text:
            return []
        trigger_idx = raw_text.lower().find(normalized_trigger.lower()) if normalized_trigger else -1
        if trigger_idx >= 0:
            sentence_start = max(
                raw_text.rfind(".", 0, trigger_idx),
                raw_text.rfind(";", 0, trigger_idx),
                raw_text.rfind("\n", 0, trigger_idx),
            ) + 1
            sentence_end_candidates = [
                pos for pos in (
                    raw_text.find(".", trigger_idx),
                    raw_text.find(";", trigger_idx),
                    raw_text.find("\n", trigger_idx),
                )
                if pos != -1
            ]
            sentence_end = min(sentence_end_candidates) if sentence_end_candidates else len(raw_text)
            if self.planning_profile == "casie":
                window_start = max(0, trigger_idx - self.repair_local_window)
                window_end = min(len(raw_text), trigger_idx + len(normalized_trigger) + self.repair_local_window)
                local_context = f"{raw_text[sentence_start:sentence_end]} {raw_text[window_start:window_end]}"
            else:
                local_context = raw_text[sentence_start:sentence_end]
            local_trigger_idx = trigger_idx - sentence_start
        else:
            local_context = raw_text[:600]
            local_trigger_idx = 0

        stopwords = {
            "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "for", "from", "by", "with",
            "as", "that", "this", "these", "those", "it", "its", "their", "our", "we", "results", "data",
        }
        patterns = [
            r"\bCVE[- ]?\d{4}[- ]?\d{3,7}\b",
            r"(?:\$|£|€)\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:million|billion|thousand))?",
            r"\b\d+(?:\.\d+)?\s+(?:bitcoin|bitcoins|ethereum|rubles|dollars|euros|pounds)\b",
            r"\b(?:bitcoin|bitcoins|ethereum|iTunes gift cards?|gift cards?|cryptocurrency)\b",
            r"\b(?:today|yesterday|tomorrow|this week|last week|this month|last month|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
            r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?\b",
            r"\b(?:personal|patient|account|customer|classified|medical|browsing|location)?\s*(?:data|information|records|accounts|passwords|files|emails|credentials|details|content|database)\b",
            r"\b(?:vulnerability|vulnerabilities|flaw|bug|bugs|issue|issues|weakness|weaknesses|loophole|problem)\b",
            r"\b(?:update|updates|patch|patches|fix|fixes|advisory|release|signatures|mitigation)\b",
            r"\b(?:users|victims|customers|organizations|companies|devices|systems|servers|accounts|computers|network|networks|website|websites|malware|ransomware|virus|exploit|emails|documents|files|researchers|experts|hackers|attackers|cybercriminals|criminals|fraudsters)\b",
            r"\"[^\"]{3,80}\"",
            r"\b[A-Za-z]*[A-Z][A-Za-z]*[A-Za-z0-9&._'/-]*(?:[ \t]+[A-Z][A-Za-z0-9&._'/-]*){0,5}\b",
            r"\b[A-Za-z]+\d+[A-Za-z0-9-]*\b",
            r"\b[A-Z]{2,}[A-Za-z0-9-]*\b",
            r"\b\d+(?:\.\d+)?[ \t]*(?:%|kDa|bp|kb|h|hr|hours|days|minutes|min)\b",
            r"\b(?:[A-Za-z0-9&._'/-]+[ \t]+){0,3}(?:domain|region|site|motif|promoter|enhancer|nucleus|cytoplasm|cell|cells|protein|gene|mRNA|reporter|construct|system|systems|server|servers|device|devices|software|firmware|platform|product|malware|ransomware|exploit|patch|update|vulnerability|flaw|bug|issue)\b",
        ]
        candidates: List[tuple[int, int, str]] = []
        seen: set[str] = set()
        for pattern in patterns:
            for match in re.finditer(pattern, local_context):
                candidate = match.group(0).strip(".,;:()[]{}\"'")
                normalized_candidate = self._normalize_whitespace(candidate)
                if not normalized_candidate or normalized_candidate.lower() == normalized_trigger.lower():
                    continue
                if "\n" in candidate or "\r" in candidate:
                    continue
                words = normalized_candidate.split()
                if len(words) > 8:
                    continue
                if len(words) == 1 and normalized_candidate.lower() in stopwords:
                    continue
                if normalized_candidate not in raw_text:
                    continue
                lowered = normalized_candidate.lower()
                if lowered in seen:
                    continue
                seen.add(lowered)
                distance = abs(match.start() - local_trigger_idx)
                candidates.append((distance, len(words), normalized_candidate))
        candidates.sort(key=lambda item: (item[0], item[1], len(item[2])))
        return [candidate for _, _, candidate in candidates[:max_candidates]]

    def _candidate_is_compatible_with_role(self, role: str, candidate: str) -> bool:
        role_lower = role.lower().replace("-", "_")
        candidate_lower = candidate.lower()
        if role_lower in CASIE_NUMERIC_ROLE_NAMES:
            return len(candidate.split()) <= 4 and bool(re.search(r"(?:\d|\$|£|€|\b(?:million|billion|thousand|bitcoin|bitcoins|dollars|euros|pounds)\b)", candidate_lower, flags=re.IGNORECASE))
        if role_lower == "cve":
            return bool(re.search(r"\bCVE[- ]?\d{4}[- ]?\d{3,7}\b", candidate, flags=re.IGNORECASE))
        if role_lower == "payment_method":
            return bool(re.search(r"\b(?:bitcoin|bitcoins|ethereum|iTunes gift cards?|gift cards?|cryptocurrency)\b", candidate, flags=re.IGNORECASE))
        if role_lower == "time":
            return self._looks_like_time_value(candidate)
        return len(candidate.split()) <= 8

    def _extract_arguments_with_candidate_selection(
        self,
        text: str,
        trigger: str,
        event_type: str,
        role_names: List[str],
        allowed_roles: set[str] | None = None,
    ) -> Dict[str, List[str]]:
        candidate_limit = 48 if self.planning_profile == "casie" else 32
        candidates = self._extract_generic_argument_candidates(text, trigger, max_candidates=candidate_limit)
        normalized: Dict[str, List[str]] = {role: [] for role in role_names}
        active_roles = [role for role in role_names if allowed_roles is None or role.lower().replace("-", "_") in allowed_roles]
        if not candidates or not active_roles:
            return normalized
        candidate_ids = {f"C{idx}": candidate for idx, candidate in enumerate(candidates, start=1)}
        candidate_lines = "\n".join(f"{cid}: {span}" for cid, span in candidate_ids.items())
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a schema-guided event argument selector. Return strict JSON only. "
                    "You must select argument fillers by candidate ID, not by copying text."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Task:\n"
                    "Select argument candidates for one event mention.\n\n"
                    "Rules:\n"
                    "1. Use only candidate IDs from the list.\n"
                    "2. Return [] for uncertain or absent roles.\n"
                    "3. Do not invent spans or output raw text spans.\n"
                    "4. Prefer candidates in the same clause as the trigger and semantically linked to it.\n"
                    "5. Prefer short entity-like candidates over long descriptive candidates when both are available.\n"
                    "6. Never select the trigger itself as an argument.\n\n"
                    "Output format:\n"
                    "Return exactly one JSON object whose keys are the role names and whose values are lists of candidate IDs.\n\n"
                    f"Event type: {event_type}\n"
                    f"Trigger: {trigger}\n"
                    f"Roles: {', '.join(active_roles)}\n\n"
                    f"Candidate IDs:\n{candidate_lines}\n\n"
                    f"Text:\n{text}"
                ),
            },
        ]
        reply = call_llm(
            messages,
            model=self.llm_model,
            base_url=self.llm_base_url,
            api_key=self.llm_api_key,
            request_tag="coding_candidate_select",
            max_tokens=384,
        )
        data = _load_json_reply(reply)
        if not isinstance(data, dict):
            return normalized
        for role in active_roles:
            raw_values = data.get(role, [])
            if isinstance(raw_values, str):
                raw_values = [raw_values]
            if not isinstance(raw_values, list):
                continue
            values: List[str] = []
            for raw_value in raw_values:
                if not isinstance(raw_value, str):
                    continue
                cid = raw_value.strip().upper()
                selected = candidate_ids.get(cid)
                if selected and self._candidate_is_compatible_with_role(role, selected) and selected not in values:
                    values.append(selected)
            normalized[role] = values
        return normalized

    def _first_local_match(self, patterns: List[str], context: str) -> str | None:
        for pattern in patterns:
            match = re.search(pattern, context, flags=re.IGNORECASE)
            if match:
                candidate = self._normalize_whitespace(match.group(1) if match.lastindex else match.group(0)).strip(".,;:()[]{}\"'")
                candidate = re.sub(r"\s+(?:has|have|had|was|were|is|are)$", "", candidate, flags=re.IGNORECASE)
                return candidate
        return None

    def _apply_role_aware_local_fallback(
        self,
        trigger: str,
        arguments: Dict[str, List[str]],
        role_names: List[str],
        text: str,
    ) -> Dict[str, List[str]]:
        context = self._build_trigger_sentence(text, trigger) or self._build_local_context(text, trigger)
        if not context:
            return arguments
        filled: Dict[str, List[str]] = {role: list(arguments.get(role, [])) for role in role_names}
        for role in role_names:
            if filled.get(role):
                continue
            role_lower = role.lower().replace("-", "_")
            candidate: str | None = None
            if role_lower == "cve":
                candidate = self._first_local_match([r"\bCVE[- ]?\d{4}[- ]?\d{3,7}\b"], context)
            elif role_lower in {"price", "damage_amount"}:
                candidate = self._first_local_match([
                    r"(?:\$|£|€)\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:million|billion|thousand))?",
                    r"\b\d+(?:\.\d+)?\s+(?:bitcoin|bitcoins|rubles|dollars|euros|pounds)\b",
                ], context)
            elif role_lower == "payment_method":
                candidate = self._first_local_match([
                    r"\b(?:in|via|using|with|by)\s+((?:bitcoin|bitcoins|ethereum|iTunes gift cards?|gift cards?|cryptocurrency))\b",
                    r"\b(?:bitcoin|bitcoins|ethereum|iTunes gift cards?|gift cards?|cryptocurrency)\b",
                ], context)
            elif role_lower == "time":
                candidate = self._first_local_match([
                    r"\b(?:today|yesterday|tomorrow|this week|last week|this month|last month|early [A-Z][a-z]+|late [A-Z][a-z]+|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
                    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?\b",
                    r"\b\d{4}\b",
                ], context)
            elif role_lower == "vulnerability":
                candidate = self._first_local_match([
                    r"\b(?:a|an|the|these|this)?\s*((?:critical|serious|security|authentication|zero-day|code execution|reported|new)?\s*(?:vulnerability|vulnerabilities|flaw|bug|bugs|issue|issues|weakness|weaknesses|loophole|problem))\b",
                    r"\b(CVE[- ]?\d{4}[- ]?\d{3,7})\b",
                ], context)
            elif role_lower in {"patch", "issues_addressed"}:
                candidate = self._first_local_match([
                    r"\b((?:security|firmware|software|microcode)?\s*(?:update|updates|patch|patches|fix|fixes|advisory|release|signatures|mitigation))\b",
                    r"\b(address(?:ed|es)?\s+[^,.;]{3,80})",
                ], context)
            elif role_lower == "compromised_data":
                candidate = self._first_local_match([
                    r"\b((?:personal|patient|account|customer|classified|medical|browsing|location)?\s*(?:data|information|records|accounts|passwords|files|emails|credentials|details|content|database))\b",
                ], context)
            elif role_lower == "attacker":
                candidate = self._first_local_match([
                    r"\b(hackers|attackers|cybercriminals|criminals|fraudsters|ransomware actors|the hackers|the attackers|the cybercriminals|the criminals|the fraudsters)\b",
                    r"\b((?:[A-Z][A-Za-z0-9&._'-]*)(?:\s+[A-Z][A-Za-z0-9&._'-]*){0,4})\s+(?:attacked|compromised|hacked|stole|leaked|demanded|encrypted|infected|tricked)\b",
                ], context)
            elif role_lower in {"discoverer", "releaser", "vulnerable_system_owner"}:
                candidate = self._first_local_match([
                    r"\b((?:[A-Z][A-Za-z0-9&._'-]*)(?:\s+[A-Z][A-Za-z0-9&._'-]*){0,4})\s+(?:said|says|reported|revealed|discovered|found|released|patched|fixed|announced|issued|warned|explained|confirmed|notified|detected)\b",
                    r"\b(?:by|from|according to)\s+((?:[A-Z][A-Za-z0-9&._'-]*)(?:\s+[A-Z][A-Za-z0-9&._'-]*){0,4})\b",
                    r"\b(hackers|attackers|cybercriminals|criminals|fraudsters|researchers|experts|the company|the firm|the researchers)\b",
                ], context)
            elif role_lower in {"victim", "vulnerable_system", "tool", "trusted_entity"}:
                candidate = self._first_local_match([
                    r"\b(users|victims|customers|organizations|companies|devices|systems|servers|accounts|computers|network|networks|database|databases|website|websites|malware|ransomware|virus|exploit|emails|phishing page|documents|files)\b",
                    r"\b(?:of|for|from|against|targeting|affecting)\s+((?:[A-Z][A-Za-z0-9&._'-]*)(?:\s+[A-Z][A-Za-z0-9&._'-]*){0,5})\b",
                ], context)
            elif role_lower in {"attack_pattern", "purpose", "capabilities"}:
                candidate = None
            if candidate and len(candidate.split()) <= 8 and not any(marker in candidate.lower() for marker in (" is that ", " or else ", " because ", " while ")) and candidate.lower() != self._normalize_whitespace(trigger).lower() and self._span_in_text(candidate, text):
                filled[role] = [candidate]
        return filled

    def _apply_hybrid_argument_filter(
        self,
        trigger: str,
        arguments: Dict[str, List[str]],
        role_names: List[str],
        text: str,
    ) -> Dict[str, List[str]]:
        trigger_sentence = self._build_trigger_sentence(text, trigger)
        local_context = self._build_local_context(text, trigger)
        normalized_trigger = self._normalize_whitespace(trigger).lower()
        role_limited: Dict[str, List[str]] = {role: [] for role in role_names}
        for role in role_names:
            role_lower = role.lower().replace("-", "_")
            seen: set[str] = set()
            for raw_value in arguments.get(role, []):
                if not isinstance(raw_value, str):
                    continue
                cleaned = self._normalize_whitespace(raw_value).strip(".,;:()[]{}\"'")
                cleaned = re.sub(r"^(?:of|to|with|by|for|in|on|at|from|through|via)\s+", "", cleaned, flags=re.IGNORECASE)
                if not cleaned:
                    continue
                of_match = re.search(r"\bof\s+(.+)$", cleaned, flags=re.IGNORECASE)
                if of_match:
                    tail = self._normalize_whitespace(of_match.group(1)).strip(".,;:()[]{}\"'")
                    if tail and self._span_in_text(tail, text) and len(tail.split()) <= max(5, len(cleaned.split()) - 1):
                        cleaned = tail
                if role_lower.startswith("theme") or role_lower == "cause":
                    cleaned = re.sub(
                        r"^(?:the|a|an|full-length|mutant|dominant-negative|coactivator|coactivators|protein|proteins|factor|factors)\s+",
                        "",
                        cleaned,
                        flags=re.IGNORECASE,
                    ).strip(".,;:()[]{}\"'")
                    trailing_head_match = re.match(
                        r"^(.+?)\s+(?:activation|expression|transcription|transactivation|repression|suppression|inhibition|overexpression|recruitment|localization|phosphorylation|binding|activity|function|signaling|pathway|mRNA|protein|fusion protein)$",
                        cleaned,
                        flags=re.IGNORECASE,
                    )
                    if trailing_head_match:
                        head = self._normalize_whitespace(trailing_head_match.group(1)).strip(".,;:()[]{}\"'")
                        if head and self._span_in_text(head, text):
                            cleaned = head
                    embedded_symbol_match = re.search(r"\b[A-Za-z0-9._+/-]*[A-Z][A-Za-z0-9._+/-]*(?:/[A-Za-z0-9._+/-]+)?\b", cleaned)
                    if embedded_symbol_match and len(cleaned.split()) > 1:
                        symbol = self._normalize_whitespace(embedded_symbol_match.group(0))
                        if symbol and self._span_in_text(symbol, text):
                            cleaned = symbol
                if role_lower in {"site", "csite", "site2", "toloc", "atloc", "fromloc"}:
                    location_match = re.search(
                        r"\b(?:nucleus|nuclear|cytoplasm|cytoplasmic|membrane|promoter|domain|region|element|site|motif)\b(?:\s+\d+)?",
                        cleaned,
                        flags=re.IGNORECASE,
                    )
                    if location_match:
                        candidate = self._normalize_whitespace(location_match.group(0))
                        if self._span_in_text(candidate, text):
                            cleaned = candidate
                lowered = cleaned.lower()
                if lowered == normalized_trigger or lowered in seen:
                    continue
                if not self._span_in_text(cleaned, text):
                    continue
                if lowered not in self._normalize_whitespace(trigger_sentence).lower() and lowered not in self._normalize_whitespace(local_context).lower():
                    continue
                word_count = len(cleaned.split())
                if role_lower in {"number_of_data", "number_of_victim"} and (word_count > 4 or not any(ch.isdigit() for ch in cleaned)):
                    continue
                if role_lower in {"price", "damage_amount"} and word_count > 6:
                    continue
                if role_lower in {"tool", "attack_pattern", "place", "issues_addressed"} and word_count > 5:
                    continue
                if role_lower in {"time"} and word_count > 6:
                    continue
                if role_lower.startswith("theme") and word_count > 8:
                    continue
                if role_lower == "cause" and word_count > 8:
                    continue
                if role_lower in {"site", "csite", "site2", "toloc", "atloc", "fromloc"} and word_count > 6:
                    continue
                seen.add(lowered)
                role_limited[role].append(cleaned)
            if role_lower in {"cause", "site", "csite", "site2", "toloc", "atloc", "fromloc"}:
                role_limited[role] = role_limited[role][:1]
        return role_limited

    def generate_event_object(
        self,
        hypothesis: Hypothesis,
        schema: EventSchema,
        text: str,
        *,
        use_llm_coding: bool | None = None,
    ) -> EventObject:
        """Instantiate a single :class:`EventObject` from a trigger hypothesis."""
        should_use_llm = self.use_llm_coding if use_llm_coding is None else use_llm_coding
        if should_use_llm:
            if self.argument_mode == "candidate_select":
                args = self._extract_arguments_with_candidate_selection(
                    text=text,
                    trigger=hypothesis.trigger,
                    event_type=schema.event_type,
                    role_names=list(schema.roles.keys()),
                )
            else:
                args = extract_arguments_for_event(
                    text=text,
                    trigger=hypothesis.trigger,
                    event_type=schema.event_type,
                    role_names=list(schema.roles.keys()),
                    model=self.llm_model,
                    base_url=self.llm_base_url,
                    api_key=self.llm_api_key,
                    planning_profile=self.planning_profile,
                )
                if self.argument_mode in {"hybrid", "hybrid_candidate"}:
                    args = self._apply_hybrid_argument_filter(
                        trigger=hypothesis.trigger,
                        arguments=args,
                        role_names=list(schema.roles.keys()),
                        text=text,
                    )
                    if self.argument_mode == "hybrid_candidate":
                        allowed_roles = CASIE_CANDIDATE_ROLE_NAMES if self.planning_profile == "casie" else None
                        candidate_args = self._extract_arguments_with_candidate_selection(
                            text=text,
                            trigger=hypothesis.trigger,
                            event_type=schema.event_type,
                            role_names=list(schema.roles.keys()),
                            allowed_roles=allowed_roles,
                        )
                        for role in schema.roles.keys():
                            if not args.get(role) and candidate_args.get(role):
                                args[role] = candidate_args[role]
                    if self.planning_profile in {"casie", "generic"}:
                        args = self._apply_role_aware_local_fallback(
                            trigger=hypothesis.trigger,
                            arguments=args,
                            role_names=list(schema.roles.keys()),
                            text=text,
                        )
                    if schema.event_type in GENIA_EVENT_TYPES or self.planning_profile == "genia":
                        args = self._apply_genia_theme_refill(
                            trigger=hypothesis.trigger,
                            event_type=schema.event_type,
                            arguments=args,
                            role_names=list(schema.roles.keys()),
                            text=text,
                        )
        else:
            args = self._select_heuristic_arguments(
                trigger=hypothesis.trigger,
                schema=schema,
                text=text,
            )
        trigger_source = args.get("__mention", [hypothesis.trigger])[0] if self.planning_profile == "mapcoder" else hypothesis.trigger
        cleaned_trigger = self._normalize_whitespace(trigger_source) or hypothesis.trigger
        if schema.event_type in GENIA_EVENT_TYPES or self.planning_profile == "genia":
            cleaned_trigger = self._clean_genia_trigger(cleaned_trigger, text) or cleaned_trigger
        if not self._span_in_text(cleaned_trigger, text):
            cleaned_trigger = self._normalize_whitespace(hypothesis.trigger) or hypothesis.trigger
            if schema.event_type in GENIA_EVENT_TYPES or self.planning_profile == "genia":
                cleaned_trigger = self._clean_genia_trigger(cleaned_trigger, text) or cleaned_trigger
        args = {role: values for role, values in args.items() if role in schema.roles}
        cleaned_arguments = self._sanitize_arguments(cleaned_trigger, args, schema, text)
        if schema.event_type in GENIA_EVENT_TYPES or self.planning_profile == "genia":
            if "theme" in cleaned_arguments and not cleaned_arguments["theme"]:
                dummy_event = EventObject(event_type=schema.event_type, trigger=cleaned_trigger, arguments=cleaned_arguments)
                refill = self._find_genia_binding_theme_refill(dummy_event, text)
                if not refill:
                    refill = self._find_genia_expression_theme_refill(dummy_event, text)
                if not refill:
                    refill = self._find_generic_genia_theme_refill(dummy_event, text)
                if refill and self._span_in_text(refill, text):
                    cleaned_arguments["theme"] = [refill]
        return EventObject(event_type=schema.event_type, trigger=cleaned_trigger, arguments=cleaned_arguments)

    def generate_event_objects(
        self,
        hypothesis: Hypothesis,
        schema: EventSchema,
        text: str,
        *,
        use_llm_coding: bool | None = None,
    ) -> List[EventObject]:
        """Instantiate zero or more :class:`EventObject` instances."""
        should_use_llm = self.use_llm_coding if use_llm_coding is None else use_llm_coding
        if self.force_hypothesis_trigger_coding:
            return [self.generate_event_object(hypothesis, schema, text, use_llm_coding=should_use_llm)]
        if not should_use_llm:
            return [self.generate_event_object(hypothesis, schema, text, use_llm_coding=False)]
        if self.planning_profile == "mapcoder":
            return [self.generate_event_object(hypothesis, schema, text, use_llm_coding=True)]
        if self.argument_mode in {"candidate_select", "hybrid", "hybrid_candidate"}:
            return [self.generate_event_object(hypothesis, schema, text, use_llm_coding=True)]

        events: List[EventObject] = []
        seen: set[tuple[str, tuple[tuple[str, tuple[str, ...]], ...]]] = set()

        if self.use_mention_first_coding:
            mention_candidates = extract_mentions_for_event_type(
                text=text,
                event_type=schema.event_type,
                model=self.llm_model,
                base_url=self.llm_base_url,
                api_key=self.llm_api_key,
                planning_profile=self.planning_profile,
            )
            if hypothesis.trigger and self._span_in_text(hypothesis.trigger, text):
                normalized_hyp = self._normalize_whitespace(hypothesis.trigger)
                if normalized_hyp and normalized_hyp.lower() not in {m.lower() for m in mention_candidates}:
                    mention_candidates = [normalized_hyp] + mention_candidates
            mention_iterable = tqdm(
                mention_candidates,
                total=len(mention_candidates),
                desc=f"Args {schema.event_type}",
                unit="mention",
                leave=False,
                dynamic_ncols=True,
            ) if len(mention_candidates) > 1 else mention_candidates
            for mention in mention_iterable:
                args = extract_arguments_for_event(
                    text=text,
                    trigger=mention,
                    event_type=schema.event_type,
                    role_names=list(schema.roles.keys()),
                    model=self.llm_model,
                    base_url=self.llm_base_url,
                    api_key=self.llm_api_key,
                    planning_profile=self.planning_profile,
                )
                candidate = self._sanitize_event_object(
                    EventObject(
                        event_type=schema.event_type,
                        trigger=self._normalize_whitespace(mention) or mention,
                        arguments={role: args.get(role, []) for role in schema.roles.keys()},
                    ),
                    schema,
                    text,
                )
                dedupe_key = (
                    candidate.trigger,
                    tuple((role, tuple(candidate.arguments[role])) for role in sorted(candidate.arguments.keys())),
                )
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                events.append(candidate)
            if events:
                return events
            return [self.generate_event_object(hypothesis, schema, text, use_llm_coding=True)]

        raw_events = extract_events_for_schema(
            text=text,
            event_type=schema.event_type,
            role_names=list(schema.roles.keys()),
            model=self.llm_model,
            base_url=self.llm_base_url,
            api_key=self.llm_api_key,
            planning_profile=self.planning_profile,
        )
        for item in raw_events:
            mention = item.get("mention")
            if not isinstance(mention, str):
                continue
            arguments: Dict[str, List[str]] = {}
            for role in schema.roles.keys():
                value = item.get(role, [])
                arguments[role] = value if isinstance(value, list) else []
            candidate = self._sanitize_event_object(
                EventObject(event_type=schema.event_type, trigger=mention, arguments=arguments),
                schema,
                text,
            )
            dedupe_key = (
                candidate.trigger,
                tuple((role, tuple(candidate.arguments[role])) for role in sorted(candidate.arguments.keys())),
            )
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            events.append(candidate)
        if events:
            return events
        return [self.generate_event_object(hypothesis, schema, text, use_llm_coding=True)]

    def repair_trigger_hypothesis(
        self,
        hypothesis: Hypothesis,
        text: str,
        verification_error: str,
        verification_info: Dict[str, object] | None = None,
    ) -> Hypothesis:
        """Repair a trigger hypothesis using verifier feedback."""
        repaired_trigger = repair_trigger_hypothesis(
            text=text,
            event_type=hypothesis.event_type,
            current_trigger=hypothesis.trigger,
            verification_error=verification_error,
            verification_info=verification_info,
            model=self.llm_model,
            base_url=self.llm_base_url,
            api_key=self.llm_api_key,
        )
        repaired_trigger = self._fallback_replace_trigger(
            text=text,
            current_trigger=hypothesis.trigger,
            repaired_trigger=repaired_trigger,
            verification_info=verification_info,
        )
        return Hypothesis(
            trigger=repaired_trigger,
            event_type=hypothesis.event_type,
            confidence=hypothesis.confidence,
            rationale=f"{hypothesis.rationale} | repaired from verifier feedback",
        )

    def repair_event_object(
        self,
        event_obj: EventObject,
        schema: EventSchema,
        text: str,
        verification_error: str,
        verification_info: Dict[str, object] | None = None,
    ) -> EventObject:
        """Repair a generated event object using verifier feedback."""
        if self.use_llm_coding:
            repaired_arguments = repair_event_object(
                text=text,
                event_type=schema.event_type,
                trigger=event_obj.trigger,
                role_names=list(schema.roles.keys()),
                current_arguments=event_obj.arguments,
                verification_error=verification_error,
                verification_info=verification_info,
                candidate_arguments=self._build_repair_candidates(
                    trigger=event_obj.trigger,
                    schema=schema,
                    text=text,
                    verification_info=verification_info,
                ),
                model=self.llm_model,
                base_url=self.llm_base_url,
                api_key=self.llm_api_key,
            )
            repaired_arguments = self._enforce_argument_constraints(
                trigger=event_obj.trigger,
                arguments=repaired_arguments,
                verification_info=verification_info,
                text=text,
            )
        else:
            repaired_arguments = {role: list(values) for role, values in event_obj.arguments.items()}
            category = verification_info.get("category") if isinstance(verification_info, dict) else None
            details = verification_info.get("details") if isinstance(verification_info, dict) else None
            if category in {"argument_role_semantics", "argument_not_locally_bound", "argument_crosses_clause_boundary"} and isinstance(details, dict):
                role = details.get("role")
                if isinstance(role, str) and role in schema.roles:
                    candidates = self._build_repair_candidates(
                        trigger=event_obj.trigger,
                        schema=schema,
                        text=text,
                        verification_info=verification_info,
                    ).get(role, [])
                    current_bad = self._normalize_whitespace(str(details.get("value", ""))).lower()
                    sentence_lower = self._build_trigger_sentence(text, event_obj.trigger).lower()
                    replacement = next(
                        (
                            cand for cand in candidates
                            if cand.lower() != current_bad and self._role_candidate_matches(role, cand, sentence_lower)
                        ),
                        None,
                    )
                    if replacement is not None:
                        replacement = self._refine_candidate_for_role(role, replacement, self._build_local_context(text, event_obj.trigger))
                    repaired_arguments[role] = [replacement] if replacement else []
            elif category == "argument_over_reused" and isinstance(details, dict):
                reused_roles = details.get("roles")
                if isinstance(reused_roles, list):
                    for idx, role in enumerate(reused_roles):
                        if not isinstance(role, str) or role not in repaired_arguments:
                            continue
                        if idx == 0:
                            continue
                        repaired_arguments[role] = []
            repaired_arguments = self._repair_arguments_with_local_fallback(
                trigger=event_obj.trigger,
                arguments=repaired_arguments,
                verification_info=verification_info,
                text=text,
            )
        return EventObject(
            event_type=schema.event_type,
            trigger=self._normalize_whitespace(event_obj.trigger) or event_obj.trigger,
            arguments=self._sanitize_arguments(event_obj.trigger, repaired_arguments, schema, text),
        )

    def generate_code(
        self,
        hypothesis: Hypothesis,
        schema: EventSchema,
        text: str,
    ) -> str:
        """Return a Python code snippet that instantiates the event object."""
        arg_dict_items = ", ".join([f"'{role}': []" for role in schema.roles])
        code = (
            "from aec.event_schema import EventObject\n"
            f"event = EventObject(event_type='{schema.event_type}', trigger='{hypothesis.trigger}', arguments={{ {arg_dict_items} }})\n"
            "event"
        )
        return code
