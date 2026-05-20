"""Retrieval agent for schema-aware exemplar selection."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, List, Optional

try:
    from .event_schema import EventSchema
except ImportError:
    from event_schema import EventSchema


@dataclass
class RetrievalAgent:
    """A simple retrieval agent."""

    example_db: Optional[Dict[str, List[str]]] = None

    _tokeniser = re.compile(r"\b\w+\b", re.UNICODE)

    def _schema_keywords(self, schema: EventSchema) -> set[str]:
        keywords = set()
        for token in self._tokeniser.findall(schema.event_type.lower()):
            if len(token) >= 3:
                keywords.add(token)
        for role in schema.roles.keys():
            for token in self._tokeniser.findall(role.lower()):
                if len(token) >= 3:
                    keywords.add(token)
        return keywords

    def _score_example(self, schema: EventSchema, example: str) -> tuple[int, int, int]:
        lowered = example.lower()
        keyword_hits = sum(1 for keyword in self._schema_keywords(schema) if keyword in lowered)
        role_hits = sum(1 for role in schema.roles.keys() if role.lower() in lowered)
        event_hit = 1 if schema.event_type.lower() in lowered else 0
        return event_hit, keyword_hits, role_hits

    def _rank_examples(self, schema: EventSchema, examples: List[str], k: int) -> List[str]:
        ranked = sorted(examples, key=lambda example: self._score_example(schema, example), reverse=True)
        deduped: List[str] = []
        seen: set[str] = set()
        for example in ranked:
            key = " ".join(example.lower().split())
            if key in seen:
                continue
            seen.add(key)
            deduped.append(example)
            if len(deduped) >= k:
                break
        return deduped

    def _build_schema_aware_examples(self, schema: EventSchema, k: int) -> List[str]:
        role_names = list(schema.roles.keys())
        core_roles = ", ".join(role_names[: min(3, len(role_names))])
        examples = [
            f"Event type '{schema.event_type}': identify the exact trigger phrase in the text and verify that it truly expresses this event.",
            f"For '{schema.event_type}', do not guess from topic words alone. Prefer a trigger-centered reading where each extracted role is directly supported by the sentence and linked to the same trigger mention.",
        ]
        if core_roles:
            examples.append(
                f"Event type '{schema.event_type}': look for a trigger phrase that explicitly evokes this event, then anchor arguments around that same mention. Start by checking likely core roles such as {core_roles}."
            )
            role_descriptions = []
            for role_name, role_type in schema.roles.items():
                type_name = getattr(role_type, "__name__", str(role_type))
                role_descriptions.append(f"{role_name} ({type_name})")
            examples.append(
                f"Schema checklist for '{schema.event_type}': "
                + ", ".join(role_descriptions)
                + ". Use this as a retrieval-style reminder when ranking trigger hypotheses."
            )
        return self._rank_examples(schema, examples, max(k, 3))

    def retrieve(self, schema: EventSchema, k: int = 3) -> List[str]:
        """Return up to ``k`` exemplar sentences for the given schema."""

        if self.example_db and schema.event_type in self.example_db:
            return self._rank_examples(schema, self.example_db[schema.event_type], k)
        return self._build_schema_aware_examples(schema, k)[:k]
