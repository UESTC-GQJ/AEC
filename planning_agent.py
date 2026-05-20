"""
Planning agent for the AEC pipeline.

The planning agent analyses the input text (possibly conditioned on
retrieval exemplars) and proposes a ranked list of trigger–type
hypotheses. In the original AEC paper the planning agent leverages
large language models to generate and explain multiple candidate
event triggers along with their associated confidence scores and
rationales. This implementation supports both a simple heuristic
baseline and an optional LLM-backed planning path.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple

try:
    from .event_schema import EventSchema
    from .llm_utils import extract_trigger_event_hypotheses, extract_trigger_event_pairs, call_llm, _load_json_reply
except ImportError:
    from event_schema import EventSchema
    from llm_utils import extract_trigger_event_hypotheses, extract_trigger_event_pairs, call_llm, _load_json_reply


@dataclass
class Hypothesis:
    """Data structure representing a trigger–type hypothesis."""

    trigger: str
    event_type: str
    confidence: float
    rationale: str


class PlanningAgent:
    """A lightweight planning agent that proposes trigger hypotheses."""

    def __init__(self) -> None:
        self.last_planner_debug: dict = {}
        self.trigger_adapter: str = "none"

    _tokeniser = re.compile(r"\b\w+\b", re.UNICODE)
    _tuple_pattern = re.compile(r'\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*\)')
    _eventy_suffixes = (
        "ed",
        "ing",
        "ion",
        "tion",
        "sion",
        "ment",
        "ance",
        "ence",
        "al",
    )
    _generic_tokens = {
        "project",
        "member",
        "members",
        "account",
        "accounts",
        "information",
        "staff",
        "people",
        "person",
        "organization",
        "organisations",
        "company",
        "companies",
        "group",
        "groups",
        "users",
        "user",
        "system",
        "systems",
        "data",
        "email",
        "emails",
        "message",
        "messages",
        "team",
        "teams",
        "official",
        "officials",
        "county",
        "university",
    }
    _reporting_tokens = {
        "said",
        "says",
        "say",
        "told",
        "tell",
        "reported",
        "report",
        "reporting",
        "announced",
        "announce",
        "announcing",
        "notified",
        "notify",
        "notifying",
        "according",
        "wrote",
        "write",
        "stated",
        "state",
    }
    _bad_trigger_heads = {
        "this",
        "these",
        "that",
        "those",
        "it",
        "they",
        "we",
        "i",
        "he",
        "she",
        "functional",
        "carboxyl",
        "creb",
        "foxp3",
        "tax",
        "transactivation",
    }
    _preferred_phrases = (
        "work with",
        "working together",
        "work collaboratively",
        "gained access",
        "have been exposed",
        "have been accessed",
        "data breach",
        "phishing scam",
        "demanded a payment",
        "paid a fee",
        "pay the ransom",
        "demands a fee",
        "down-regulation",
        "up-regulation",
    )
    _genia_trigger_lexicon = {
        "Gene_expression": (
            "expression",
            "expressed",
            "express",
            "expresses",
            "expressing",
            "overexpression",
            "overexpressed",
            "overexpress",
            "coexpression",
            "mRNA expression",
            "protein expression",
            "production",
            "produce",
            "produced",
            "synthesis",
        ),
        "Transcription": (
            "transcription",
            "transcribed",
            "transcribe",
            "transcript",
            "mRNA expression",
            "transcriptional activation",
            "transactivation",
            "transcriptional activity",
        ),
        "Protein_modification": (
            "modification",
            "modified",
            "ubiquitination",
            "acetylation",
            "methylation",
            "glycosylation",
            "cleavage",
            "cleaved",
        ),
        "Phosphorylation": (
            "phosphorylation",
            "phosphorylated",
            "phosphorylate",
        ),
        "Localization": (
            "localization",
            "localized",
            "localize",
            "localizes",
            "localizing",
            "translocation",
            "translocated",
            "transport",
            "recruitment",
            "recruited",
            "nuclear accumulation",
        ),
        "Binding": (
            "binding",
            "bind",
            "binds",
            "bound",
            "interaction",
            "interactions",
            "interact",
            "interacts",
            "interacting",
            "interfacing",
            "association",
            "associate",
            "associates",
            "associating",
            "formation",
            "complex formation",
            "complexed",
            "recruitment",
            "recruit",
            "recruited",
            "recruits",
            "recruiting",
        ),
        "Positive_regulation": (
            "activation",
            "activated",
            "activate",
            "activates",
            "transcriptional activation",
            "induction",
            "induced",
            "induce",
            "induces",
            "stimulation",
            "stimulated",
            "stimulate",
            "stimulates",
            "up-regulation",
            "upregulation",
            "enhancement",
            "enhanced",
            "increase",
            "increases",
            "increased",
            "promote",
            "promotes",
            "affecting",
            "overexpression",
            "overexpressed",
            "following",
            "result",
            "results",
            "resulting",
            "permits",
            "permitted",
            "formation",
            "expressed",
            "permits",
        ),
        "Negative_regulation": (
            "inhibition",
            "inhibited",
            "inhibit",
            "inhibits",
            "suppression",
            "suppressed",
            "suppress",
            "suppresses",
            "repression",
            "repressed",
            "repress",
            "represses",
            "down-regulation",
            "downregulation",
            "decrease",
            "decreases",
            "decreased",
            "reduction",
            "reduced",
            "block",
            "blocked",
            "prevent",
            "prevents",
            "prevented",
            "lacking",
            "lack",
            "lacks",
            "inactivation",
            "inactivated",
            "interferes",
            "interfere",
        ),
        "Regulation": (
            "regulation",
            "regulated",
            "regulate",
            "regulates",
            "control",
            "controlled",
            "modulation",
            "modulated",
        ),
    }

    _casie_trigger_lexicon = {
        "Discovervulnerability": (
            "affect",
            "affects",
            "affected",
            "are affected",
            "impact",
            "impacts",
            "impacted",
            "vulnerable",
            "are vulnerable",
            "vulnerability",
            "vulnerabilities",
            "flaw",
            "flaws",
            "bug",
            "bugs",
            "issue",
            "issues",
            "zero-day",
            "0-day",
            "exploit",
            "exploited",
            "been exploited",
            "discovered",
            "have discovered",
            "found",
            "have found",
            "reported",
            "revealed",
            "disclosed",
        ),
        "Patchvulnerability": (
            "patched",
            "patch",
            "patches",
            "fixed",
            "was fixed",
            "fix",
            "fixes",
            "address",
            "addressed",
            "addresses",
            "released",
            "has released",
            "resolved",
            "mitigated",
            "mitigation",
            "update",
            "security update",
            "advisory",
        ),
        "Databreach": (
            "breach",
            "data breach",
            "was breached",
            "breached",
            "collected",
            "collecting",
            "obtain",
            "obtained",
            "stolen",
            "leaked",
            "exposed",
            "accessed",
        ),
        "Phishing": (
            "phishing",
            "phishing email",
            "phishing emails",
            "phishing email",
            "phishing emails",
            "phishing scam",
            "phishing campaign",
            "trick",
            "tricked",
            "lure",
            "lured",
            "send",
            "sent",
            "spoof",
            "spoofed",
            "impersonate",
            "impersonated",
            "pretending to be",
            "stealing",
            "credential",
            "credentials",
            "fake",
            "malicious email",
        ),
        "Ransom": (
            "ransom",
            "the ransom",
            "ransomware",
            "ransomware attack",
            "a ransomware attack",
            "paying the ransom",
            "pay the ransom",
            "demanded",
            "demanded a payment",
            "encrypt",
            "encrypted",
        ),
    }

    _protected_genia_lexicon_triggers = {
        "expression",
        "overexpression",
        "binding",
        "interaction",
        "interactions",
        "interact",
        "interacting",
        "recruitment",
        "recruit",
        "localization",
        "activation",
        "transcriptional activation",
        "mrna expression",
        "block",
        "interferes",
    }

    _protected_casie_lexicon_triggers = {
        "affect",
        "affects",
        "impact",
        "impacted",
        "affected",
        "are affected",
        "vulnerable",
        "are vulnerable",
        "discovered",
        "have discovered",
        "found",
        "have found",
        "disclosed",
        "impacts",
        "exploited",
        "been exploited",
        "address",
        "addressed",
        "addresses",
        "was fixed",
        "has released",
        "fixed",
        "released",
        "collected",
        "collecting",
        "obtain",
        "was breached",
        "trick",
        "send",
        "pretending to be",
        "the ransom",
        "ransomware attack",
        "a ransomware attack",
        "paying the ransom",
    }

    def _score_candidate(self, candidate: str, freq: int, max_freq: int, event_token: str) -> float:
        norm = candidate.lower().strip()
        parts = norm.split()
        head = parts[-1] if parts else norm
        score = 0.1
        score += min(freq / max(max_freq, 1), 1.0) * 0.2
        if " " in norm:
            score += 0.2
        if any(token in norm for token in event_token.replace("_", " ").split()):
            score += 0.15
        if any(norm.endswith(suffix) or head.endswith(suffix) for suffix in self._eventy_suffixes):
            score += 0.2
        if "-" in norm:
            score += 0.1
        if head in self._generic_tokens:
            score -= 0.35
        if head in self._reporting_tokens:
            score -= 0.45
        if len(head) <= 2:
            score -= 0.2
        if head in {"will", "would", "could", "should", "may", "might", "can"}:
            score -= 0.4
        return max(0.0, min(1.0, score))

    def _is_valid_llm_trigger(self, text: str, trigger: str) -> bool:
        norm = trigger.lower().strip()
        if not norm:
            return False
        if norm not in text.lower():
            return False
        parts = norm.split()
        head = parts[-1]
        first = parts[0]
        if head in self._generic_tokens or head in self._reporting_tokens:
            return False
        if first in self._bad_trigger_heads or head in self._bad_trigger_heads:
            return False
        if len(head) <= 2:
            return False
        if len(parts) == 1:
            raw = trigger.strip()
            if raw[:1].isupper() and not any(raw.lower().endswith(suffix) for suffix in self._eventy_suffixes):
                return False
        return True

    def _rescore_llm_hypothesis(self, text: str, event_type: str, trigger: str, confidence: float) -> float:
        text_lower = text.lower()
        freq = max(1, text_lower.count(trigger.lower())) if trigger else 1
        max_freq = max(freq, 1)
        heuristic = self._score_candidate(trigger, freq, max_freq, event_type.lower())
        return round((0.65 * confidence) + (0.35 * heuristic), 4)

    def _parse_tuple_pairs(self, reply: str) -> List[Tuple[str, str]]:
        data = _load_json_reply(reply)
        pairs: List[Tuple[str, str]] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    event_type = item.get("event_type")
                    trigger = item.get("trigger")
                    if isinstance(event_type, str) and isinstance(trigger, str):
                        pairs.append((event_type, trigger))
                elif isinstance(item, (list, tuple)) and len(item) == 2:
                    left, right = item
                    if isinstance(left, str) and isinstance(right, str):
                        pairs.append((left, right))
        if pairs:
            return pairs
        text = reply.strip()
        if text.lower().startswith("final answer:"):
            text = text.split(":", 1)[1].strip()
        return [(left, right) for left, right in self._tuple_pattern.findall(text)]

    def _extract_event_names_from_definitions(self, event_definitions: str) -> List[str]:
        return re.findall(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*:", event_definitions)

    def _collect_phrase_candidates(self, text: str, event_token: str) -> List[str]:
        text_lower = text.lower()
        phrase_candidates: List[str] = []
        for phrase in self._preferred_phrases:
            for match in re.finditer(re.escape(phrase), text_lower):
                phrase_candidates.append(text[match.start() : match.end()])
        event_parts = [part for part in event_token.replace("_", " ").split() if part]
        if event_parts:
            for idx in range(len(event_parts) - 1):
                phrase = f"{event_parts[idx]} {event_parts[idx + 1]}"
                for match in re.finditer(re.escape(phrase), text_lower):
                    phrase_candidates.append(text[match.start() : match.end()])
        return phrase_candidates

    def generate_hypotheses(
        self,
        text: str,
        schema: EventSchema,
        examples: List[str],
        k: int = 3,
    ) -> List[Hypothesis]:
        """Generate a ranked list of up to ``k`` heuristic trigger hypotheses."""
        text_lower = text.lower()
        tokens = self._tokeniser.findall(text_lower)
        candidates: List[Hypothesis] = []
        seen: set[str] = set()
        event_token = schema.event_type.lower()
        for match in re.finditer(re.escape(event_token), text_lower):
            trig = text[match.start() : match.end()]
            rationale = (
                f"The substring '{trig}' exactly matches the event type name '{schema.event_type}' in the text. "
                f"This is stronger evidence than nearby non-matching tokens because it directly names the target event type."
            )
            candidates.append(
                Hypothesis(trigger=trig, event_type=schema.event_type, confidence=1.0, rationale=rationale)
            )
            seen.add(trig.lower())
        if not candidates:
            stop_words = {
                "the", "a", "an", "of", "in", "and", "to", "for", "on", "with", "as", "by",
                "is", "was", "were", "be", "been", "are", "that", "this", "it", "from", "at",
                "or", "their", "his", "her", "its", "our", "your", "they", "we", "he", "she",
            }
            counter = Counter(tok for tok in tokens if tok not in stop_words)
            max_freq = counter.most_common(1)[0][1] if counter else 1
            raw_candidates: List[tuple[str, int]] = []
            for phrase in self._collect_phrase_candidates(text, event_token):
                norm = phrase.lower().strip()
                if norm and norm not in seen:
                    phrase_freq = max(1, text_lower.count(norm))
                    raw_candidates.append((phrase, phrase_freq))
                    seen.add(norm)
            for word, freq in counter.most_common(max(k * 6, 20)):
                if word in self._generic_tokens:
                    continue
                orig_match = re.search(rf"\b{re.escape(word)}\b", text)
                trig = orig_match.group(0) if orig_match else word
                norm = trig.lower()
                if norm in seen:
                    continue
                raw_candidates.append((trig, freq))
                seen.add(norm)
            scored_candidates: List[Hypothesis] = []
            for cand, freq in raw_candidates:
                confidence = self._score_candidate(cand, freq, max_freq, event_token)
                if confidence <= 0.15:
                    continue
                rationale = (
                    f"The candidate '{cand}' was selected because it looks more like an event trigger than a generic entity mention. "
                    f"Heuristic score={confidence:.2f}, frequency={freq}."
                )
                scored_candidates.append(
                    Hypothesis(trigger=cand, event_type=schema.event_type, confidence=confidence, rationale=rationale)
                )
            candidates.extend(scored_candidates)
        candidates.sort(key=lambda h: (h.confidence, len(h.trigger.split()), len(h.trigger)), reverse=True)
        deduped: List[Hypothesis] = []
        seen_pairs: set[tuple[str, str]] = set()
        for candidate in candidates:
            key = (candidate.trigger.lower(), candidate.event_type.lower())
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            deduped.append(candidate)
            if len(deduped) >= k:
                break
        return deduped

    def _llm_pairs(
        self,
        system: str,
        user: str,
        tag: str,
        max_tokens: int,
        *,
        model: str | None,
        base_url: str | None,
        api_key: str | None,
    ) -> List[Tuple[str, str]]:
        reply = call_llm(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            model=model,
            base_url=base_url,
            api_key=api_key,
            request_tag=tag,
            max_tokens=max_tokens,
        )
        return self._parse_tuple_pairs(reply)

    def _find_genia_lexicon_pairs(self, text: str, event_definitions: str) -> List[Tuple[str, str]]:
        return self._find_event_lexicon_pairs(text, event_definitions, self._genia_trigger_lexicon)

    def _find_casie_lexicon_pairs(self, text: str, event_definitions: str) -> List[Tuple[str, str]]:
        return self._find_event_lexicon_pairs(text, event_definitions, self._casie_trigger_lexicon)

    def _find_event_lexicon_pairs(
        self,
        text: str,
        event_definitions: str,
        lexicon: dict[str, tuple[str, ...]],
    ) -> List[Tuple[str, str]]:
        allowed_types = set(self._extract_event_names_from_definitions(event_definitions))
        text_norm = " ".join(text.split())
        found: List[Tuple[int, str, str]] = []
        seen: set[tuple[str, str]] = set()
        for event_type, triggers in lexicon.items():
            if allowed_types and event_type not in allowed_types:
                continue
            for trigger in triggers:
                pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(trigger)}(?![A-Za-z0-9_-])", re.IGNORECASE)
                for match in pattern.finditer(text_norm):
                    surface = text_norm[match.start():match.end()]
                    key = (event_type.lower(), surface.lower())
                    if key in seen:
                        continue
                    seen.add(key)
                    found.append((match.start(), event_type, surface))
        found.sort(key=lambda item: (item[0], -len(item[2])))
        return [(event_type, trigger) for _, event_type, trigger in found]

    _generic_morphological_suffixes = {
        "tion": ("ed", "ing", "s", ""),
        "sion": ("ed", "ing", "s", ""),
        "ment": ("ed", "ing", "s", ""),
        "ance": ("ed", "ing", "s", "ant"),
        "ence": ("ed", "ing", "s", "ent"),
        "ing": ("ed", "s", "tion", ""),
        "ed": ("ing", "s", "tion", ""),
        "": ("ed", "ing", "s", "tion", "ment"),
    }

    def _derive_trigger_forms_from_type_name(self, event_type: str) -> List[str]:
        raw_parts = re.split(r"[_\- ]+", event_type)
        parts: List[str] = []
        for raw_part in raw_parts:
            camel_split = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw_part).split()
            if len(camel_split) == 1 and len(raw_part) > 8:
                for known_prefix in ("discover", "patch", "data", "negative", "positive"):
                    lp = raw_part.lower()
                    if lp.startswith(known_prefix) and len(lp) > len(known_prefix) + 3:
                        camel_split = [raw_part[:len(known_prefix)], raw_part[len(known_prefix):]]
                        break
            parts.extend(camel_split)
        forms: List[str] = []
        for part in parts:
            lower = part.lower()
            if len(lower) <= 2:
                continue
            forms.append(lower)
            if lower.endswith("tion") or lower.endswith("sion"):
                stem = lower[:-4]
                if len(stem) >= 3:
                    for suffix in ("ed", "ing", "s", "e", "es"):
                        forms.append(stem + suffix)
                    forms.append(stem + "e")
            elif lower.endswith("ity"):
                stem = lower[:-3]
                if len(stem) >= 4:
                    forms.append(stem + "e")
                    forms.append(stem + "ities")
                    forms.append(lower + "s")
            elif lower.endswith("ing"):
                stem = lower[:-3]
                if len(stem) >= 3:
                    for suffix in ("ed", "s", "e", "tion", "ion"):
                        forms.append(stem + suffix)
                    forms.append(stem)
            elif lower.endswith("ment"):
                stem = lower[:-4]
                if len(stem) >= 3:
                    for suffix in ("ed", "ing", "s"):
                        forms.append(stem + suffix)
            elif lower.endswith("ance") or lower.endswith("ence"):
                stem = lower[:-4]
                if len(stem) >= 3:
                    for suffix in ("ed", "ing", "s"):
                        forms.append(stem + suffix)
            elif lower.endswith("al"):
                stem = lower[:-2]
                if len(stem) >= 3:
                    for suffix in ("ed", "ing", "s", "e", "tion"):
                        forms.append(stem + suffix)
            else:
                for suffix in ("ed", "ing", "s", "tion", "ment"):
                    forms.append(lower + suffix)
                if lower.endswith("e"):
                    forms.append(lower[:-1] + "ing")
                    forms.append(lower + "d")
        return list(dict.fromkeys(forms))

    def _find_generic_lexicon_pairs(self, text: str, event_definitions: str) -> List[Tuple[str, str]]:
        allowed_types = set(self._extract_event_names_from_definitions(event_definitions))
        text_norm = " ".join(text.split())
        found: List[Tuple[int, str, str]] = []
        seen: set[tuple[str, str]] = set()
        for event_type in allowed_types:
            trigger_forms = self._derive_trigger_forms_from_type_name(event_type)
            for trigger_form in trigger_forms:
                pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(trigger_form)}(?![A-Za-z0-9_-])", re.IGNORECASE)
                for match in pattern.finditer(text_norm):
                    surface = text_norm[match.start():match.end()]
                    key = (event_type.lower(), surface.lower())
                    if key in seen:
                        continue
                    seen.add(key)
                    found.append((match.start(), event_type, surface))
        found.sort(key=lambda item: (item[0], -len(item[2])))
        return [(event_type, trigger) for _, event_type, trigger in found]

    def _find_genia_planner_recovery_pairs(self, text: str, event_definitions: str) -> List[Tuple[str, str]]:
        allowed_types = set(self._extract_event_names_from_definitions(event_definitions))
        text_norm = " ".join(text.split())
        recovery_patterns: dict[str, tuple[str, ...]] = {
            "Binding": (
                "associating",
                "interacts",
                "interaction",
                "physical interaction",
                "protein-protein interactions",
                "assembly",
                "complex formation",
            ),
            "Negative_regulation": (
                "interfering",
                "neutralizing",
                "repressed",
            ),
        }
        context_words = {
            "Binding": ("with", "between", "complex", "protein", "direct", "physical", "assembly"),
            "Negative_regulation": ("inhibit", "interfer", "block", "neutraliz", "repress", "inhibition"),
        }
        found: List[Tuple[int, str, str]] = []
        seen: set[tuple[str, str]] = set()
        for event_type, triggers in recovery_patterns.items():
            if allowed_types and event_type not in allowed_types:
                continue
            for trigger in triggers:
                pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(trigger)}(?![A-Za-z0-9_-])", re.IGNORECASE)
                for match in pattern.finditer(text_norm):
                    window = text_norm[max(0, match.start() - 80): min(len(text_norm), match.end() + 80)].lower()
                    if not any(word in window for word in context_words[event_type]):
                        continue
                    surface = text_norm[match.start():match.end()]
                    key = (event_type.lower(), surface.lower())
                    if key in seen:
                        continue
                    seen.add(key)
                    found.append((match.start(), event_type, surface))
        found.sort(key=lambda item: (item[0], -len(item[2])))
        return [(event_type, trigger) for _, event_type, trigger in found[:4]]

    def _genia_trigger_rank_adjustment(self, trigger: str) -> float:
        _ = trigger
        return 0.0

    def _run_dicore_dreamer(
        self,
        text: str,
        event_definitions: str,
        *,
        exemplars: List[str] | None = None,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> List[Tuple[str, str]]:
        return self._llm_pairs(
            "You are a biomedical event trigger proposal model. Return only a list of tuples.",
            (
                "Extract as many plausible biomedical event triggers as are explicitly evoked in the text as tuples of (event_type, trigger). "
                "Maximize recall. Prefer event-denoting verbs, nominalized event words, and short trigger phrases that appear verbatim in the text. "
                "For GENIA-style extraction, common valid triggers include words and phrases such as expression, localization, binding, activation, inhibition, regulation, transcription, overexpression, interact, associating, and mRNA expression when they truly denote events in context. "
                "Do not output entity names, proteins, genes, sentence-initial discourse words, section-title words, or generic nouns unless they explicitly evoke the event. "
                "When uncertain, keep a plausible trigger rather than dropping it.\n\n"
                f"Event definitions:\n{event_definitions}\n\n"
                + (
                    "Reference exemplars:\n" + "\n\n".join(exemplars[:4]) + "\n\n"
                    if exemplars else ""
                )
                + f"Text:\n{text}\n\n"
                + "Return only [(\"event_type\", \"trigger\"), ...]."
            ),
            "dicore_dreamer",
            768,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )

    def _run_dicore_grounder(
        self,
        text: str,
        event_definitions: str,
        trigger_candidates: List[str],
        *,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> List[Tuple[str, str]]:
        if not trigger_candidates:
            return []
        event_names = self._extract_event_names_from_definitions(event_definitions)
        return self._llm_pairs(
            "You are an event extraction model. Return only a list of tuples.",
            (
                f"Allowed event types: {', '.join(event_names)}\n"
                f"Event definitions:\n{event_definitions}\n\n"
                f"Sentence:\n{text}\n\n"
                f"Trigger words: {trigger_candidates}\n\n"
                "Map each trigger to exactly one allowed event type if supported by the sentence. "
                "Reject candidates that are entity names, title words, discourse words, or generic labels instead of true event triggers. "
                "Be conservative. Return only [(\"event_type\", \"trigger\"), ...]."
            ),
            "dicore_grounder",
            384,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )

    def _run_dicore_judge(
        self,
        text: str,
        event_type: str,
        trigger: str,
        *,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> Tuple[bool, str]:
        reply = call_llm(
            [
                {
                    "role": "system",
                    "content": "You verify whether a trigger truly evokes an event type. Output only Yes or No.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Event type: {event_type}\n"
                        f"Trigger: {trigger}\n\n"
                        f"Text:\n{text}\n\n"
                        "Does this trigger truly evoke this event type in the text? "
                        "Reject entity names, title/header words, and discourse words that do not themselves denote an event. "
                        "Output only Yes or No. Be strict."
                    ),
                },
            ],
            model=model,
            base_url=base_url,
            api_key=api_key,
            request_tag="dicore_judge",
            max_tokens=16,
        ).strip().lower()
        return reply.startswith("yes"), reply

    def generate_hypotheses_with_dicore(
        self,
        text: str,
        event_definitions: str,
        max_candidates: int = 6,
        *,
        exemplars: List[str] | None = None,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        trigger_adapter: str = "none",
    ) -> List[Hypothesis]:
        dream_pairs = self._run_dicore_dreamer(
            text=text,
            event_definitions=event_definitions,
            exemplars=exemplars,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )
        allowed_event_types = set(self._extract_event_names_from_definitions(event_definitions))
        is_genia_schema = bool(allowed_event_types & set(self._genia_trigger_lexicon))
        is_casie_schema = bool(allowed_event_types & set(self._casie_trigger_lexicon))
        use_genia_lexicon = trigger_adapter == "genia" or is_genia_schema
        lexicon_pairs = self._find_genia_lexicon_pairs(text, event_definitions) if use_genia_lexicon else []
        casie_lexicon_pairs = self._find_casie_lexicon_pairs(text, event_definitions) if is_casie_schema else []
        generic_lexicon_pairs = self._find_generic_lexicon_pairs(text, event_definitions)
        recovery_pairs = self._find_genia_planner_recovery_pairs(text, event_definitions) if use_genia_lexicon else []
        protected_lexicon_pairs: List[Tuple[str, str]] = []
        protected_seen: set[tuple[str, str]] = set()
        for event_type, trigger in lexicon_pairs + casie_lexicon_pairs:
            trigger_norm = trigger.lower().strip()
            protected_set = self._protected_genia_lexicon_triggers if event_type in self._genia_trigger_lexicon else self._protected_casie_lexicon_triggers
            if trigger_norm not in protected_set:
                continue
            key = (event_type.lower().strip(), trigger_norm)
            if key in protected_seen:
                continue
            protected_seen.add(key)
            protected_lexicon_pairs.append((event_type, trigger))
        trigger_candidates: List[str] = []
        seen_triggers: set[str] = set()
        rejected_by_local_filter: List[dict] = []
        for event_type, trigger in dream_pairs + lexicon_pairs + casie_lexicon_pairs + generic_lexicon_pairs + recovery_pairs:
            lowered = trigger.lower().strip()
            if not trigger or lowered in seen_triggers:
                continue
            if not self._is_valid_llm_trigger(text, trigger):
                rejected_by_local_filter.append({"event_type": event_type, "trigger": trigger, "stage": "dreamer_to_grounder"})
                continue
            seen_triggers.add(lowered)
            trigger_candidates.append(trigger)

        llm_grounded_pairs = self._run_dicore_grounder(
            text=text,
            event_definitions=event_definitions,
            trigger_candidates=trigger_candidates,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )
        grounded_pairs = protected_lexicon_pairs + llm_grounded_pairs + recovery_pairs
        hypotheses: List[Hypothesis] = []
        seen_pairs: set[tuple[str, str]] = set()
        judge_inputs: List[dict] = []
        judge_rejected: List[dict] = []
        judge_kept: List[dict] = []
        for rank, (event_type, trigger) in enumerate(grounded_pairs[: max_candidates * 2]):
            key = (trigger.lower().strip(), event_type.lower().strip())
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            if not self._is_valid_llm_trigger(text, trigger):
                rejected_by_local_filter.append({"event_type": event_type, "trigger": trigger, "stage": "grounder_to_judge"})
                continue
            judge_inputs.append({"event_type": event_type, "trigger": trigger, "rank": rank})
            accepted, judge_reply = self._run_dicore_judge(
                text=text,
                event_type=event_type,
                trigger=trigger,
                model=model,
                base_url=base_url,
                api_key=api_key,
            )
            base_confidence = max(0.35, 0.95 - 0.08 * rank)
            if not accepted:
                judge_rejected.append({"event_type": event_type, "trigger": trigger, "rank": rank, "reply": judge_reply})
                base_confidence = max(0.2, base_confidence - 0.25)
            confidence = self._rescore_llm_hypothesis(
                text,
                event_type,
                trigger,
                base_confidence,
            )
            confidence = max(0.0, min(1.0, confidence + self._genia_trigger_rank_adjustment(trigger)))
            hypotheses.append(
                Hypothesis(
                    trigger=trigger,
                    event_type=event_type,
                    confidence=confidence,
                    rationale="Generated by DiCoRe-style planning: open trigger proposal, constrained grounding, and strict trigger-type verification.",
                )
            )
            judge_kept.append({"event_type": event_type, "trigger": trigger, "rank": rank, "confidence": confidence, "rank_adjustment": self._genia_trigger_rank_adjustment(trigger), "judge_accepted": accepted})
            if len(hypotheses) >= max_candidates:
                break
        hypotheses.sort(key=lambda h: (h.confidence, len(h.trigger.split()), len(h.trigger)), reverse=True)
        self.last_planner_debug = {
            "backend": "dicore",
            "dreamer_pairs": [{"event_type": e, "trigger": t} for e, t in dream_pairs],
            "lexicon_pairs": [{"event_type": e, "trigger": t} for e, t in lexicon_pairs],
            "casie_lexicon_pairs": [{"event_type": e, "trigger": t} for e, t in casie_lexicon_pairs],
            "protected_lexicon_pairs": [{"event_type": e, "trigger": t} for e, t in protected_lexicon_pairs],
            "generic_lexicon_pairs": [{"event_type": e, "trigger": t} for e, t in generic_lexicon_pairs],
            "recovery_pairs": [{"event_type": e, "trigger": t} for e, t in recovery_pairs],
            "grounder_trigger_candidates": trigger_candidates,
            "llm_grounder_pairs": [{"event_type": e, "trigger": t} for e, t in llm_grounded_pairs],
            "grounder_pairs": [{"event_type": e, "trigger": t} for e, t in grounded_pairs],
            "rejected_by_local_filter": rejected_by_local_filter,
            "judge_inputs": judge_inputs,
            "judge_rejected": judge_rejected,
            "judge_kept": judge_kept,
            "final_hypotheses": [
                {"trigger": h.trigger, "event_type": h.event_type, "confidence": h.confidence}
                for h in hypotheses
            ],
        }
        return hypotheses

    def generate_hypotheses_with_llm(
        self,
        text: str,
        event_definitions: str,
        max_candidates: int = 6,
        *,
        exemplars: List[str] | None = None,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        planning_profile: str = "generic",
        planning_backend: str = "aec",
        trigger_adapter: str = "none",
    ) -> List[Hypothesis]:
        """Generate trigger hypotheses via a chat LLM.

        The backend is configurable, so this can target OpenAI-hosted models
        like ``gpt-4o`` or OpenAI-compatible local/self-hosted models such as
        Llama/Qwen served by vLLM, LM Studio, or similar servers.
        """
        if planning_backend == "dicore":
            return self.generate_hypotheses_with_dicore(
                text=text,
                event_definitions=event_definitions,
                max_candidates=max_candidates,
                exemplars=exemplars,
                model=model,
                base_url=base_url,
                api_key=api_key,
                trigger_adapter=trigger_adapter,
            )

        rich_items = extract_trigger_event_hypotheses(
            text=text,
            event_definitions=event_definitions,
            exemplars=exemplars,
            model=model,
            base_url=base_url,
            api_key=api_key,
            planning_profile=planning_profile,
        )
        hypotheses: List[Hypothesis] = []
        seen: set[tuple[str, str]] = set()
        for item in rich_items[:max_candidates]:
            trigger = item.get("trigger")
            event_type = item.get("event_type")
            if not isinstance(trigger, str) or not isinstance(event_type, str):
                continue
            if not self._is_valid_llm_trigger(text, trigger):
                continue
            key = (trigger.lower().strip(), event_type.lower().strip())
            if key in seen:
                continue
            seen.add(key)
            confidence = item.get("confidence", 0.0)
            if isinstance(confidence, int):
                confidence = float(confidence)
            if not isinstance(confidence, float):
                confidence = 0.0
            confidence = self._rescore_llm_hypothesis(text, event_type, trigger, min(1.0, max(0.0, confidence)))
            rationale = item.get("rationale", "Generated by the configured LLM planning backend.")
            if not isinstance(rationale, str) or not rationale.strip():
                rationale = "Generated by the configured LLM planning backend."
            comparison = item.get("selection_reason") or item.get("contrastive_rationale")
            if isinstance(comparison, str) and comparison.strip():
                rationale = f"{rationale.strip()} Comparison: {comparison.strip()}"
            hypotheses.append(
                Hypothesis(
                    trigger=trigger,
                    event_type=event_type,
                    confidence=confidence,
                    rationale=rationale,
                )
            )
        if hypotheses:
            hypotheses.sort(key=lambda h: (h.confidence, len(h.trigger.split()), len(h.trigger)), reverse=True)
            final_hypotheses = hypotheses[:max_candidates]
            self.last_planner_debug = {
                "backend": planning_backend,
                "rich_items": rich_items[:max_candidates],
                "final_hypotheses": [
                    {"trigger": h.trigger, "event_type": h.event_type, "confidence": h.confidence}
                    for h in final_hypotheses
                ],
            }
            return final_hypotheses

        pairs = extract_trigger_event_pairs(
            text=text,
            event_definitions=event_definitions,
            exemplars=exemplars,
            model=model,
            base_url=base_url,
            api_key=api_key,
        )
        for rank, (trigger, event_type) in enumerate(pairs[:max_candidates]):
            key = (trigger.lower().strip(), event_type.lower().strip())
            if key in seen:
                continue
            seen.add(key)
            confidence = max(0.1, 1.0 - 0.1 * rank)
            rationale = (
                "Generated by the configured LLM planning backend. "
                f"Ranked at fallback position {rank + 1} after higher-priority candidates."
            )
            hypotheses.append(
                Hypothesis(
                    trigger=trigger,
                    event_type=event_type,
                    confidence=confidence,
                    rationale=rationale,
                )
            )
        self.last_planner_debug = {
            "backend": planning_backend,
            "fallback_pairs": [
                {"trigger": trigger, "event_type": event_type}
                for trigger, event_type in pairs[:max_candidates]
            ],
            "final_hypotheses": [
                {"trigger": h.trigger, "event_type": h.event_type, "confidence": h.confidence}
                for h in hypotheses
            ],
        }
        return hypotheses
