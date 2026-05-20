from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List

try:
    from .event_schema import EventObject, EventSchema
except ImportError:
    from event_schema import EventObject, EventSchema


@dataclass
class VerificationError(Exception):
    message: str
    category: str
    details: Dict[str, Any]

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "category": self.category,
            "details": self.details,
        }


class VerificationAgent:
    """Lightweight verifier for trigger and argument sanity checks."""

    CLAUSE_BOUNDARY_RE = re.compile(r"[;]|\b(?:but|however|although|though|whereas|while)\b", re.IGNORECASE)
    ROLE_SEMANTIC_HINTS: Dict[str, str] = {
        "cve": r"\bCVE[- ]?\d{4}[- ]?\d{3,7}\b",
        "payment_method": r"\b(?:bitcoin|bitcoins|ethereum|gift cards?|cryptocurrency|wire transfer)\b",
        "time": r"\b(?:today|yesterday|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|march|april|may|june|july|august|september|october|november|december|\d{4})\b",
        "price": r"(?:\$|£|€)\s?\d|\b\d+(?:\.\d+)?\s*(?:bitcoin|bitcoins|dollars|euros|pounds)\b",
    }

    def verify(self, event_obj: EventObject, schema: EventSchema, text: str) -> bool:
        if event_obj.event_type != schema.event_type:
            raise VerificationError(
                f"Event type mismatch: expected {schema.event_type!r}, got {event_obj.event_type!r}.",
                "event_type_mismatch",
                {"expected": schema.event_type, "actual": event_obj.event_type},
            )

        trigger = self._normalize_whitespace(event_obj.trigger)
        if not trigger or trigger.lower() not in self._normalize_whitespace(text).lower():
            raise VerificationError(
                f"Trigger {event_obj.trigger!r} was not found in the source text.",
                "trigger_not_in_text",
                {"trigger": event_obj.trigger},
            )

        for role, values in event_obj.arguments.items():
            if role not in schema.roles:
                continue
            if not isinstance(values, list):
                raise VerificationError(
                    f"Role {role!r} must be a list of spans.",
                    "argument_role_semantics",
                    {"role": role, "value": values},
                )
            for value in values:
                if not isinstance(value, str):
                    raise VerificationError(
                        f"Role {role!r} contains a non-string span.",
                        "argument_role_semantics",
                        {"role": role, "value": value},
                    )
                self._verify_argument(trigger, role, value, text)
        return True

    def _verify_argument(self, trigger: str, role: str, value: str, text: str) -> None:
        cleaned = self._normalize_whitespace(value)
        if not cleaned:
            raise VerificationError(
                f"Role {role!r} contains an empty argument span.",
                "argument_role_semantics",
                {"role": role, "value": value},
            )
        if cleaned.lower() not in self._normalize_whitespace(text).lower():
            raise VerificationError(
                f"Argument span {value!r} for role {role!r} is not grounded in the text.",
                "argument_not_locally_bound",
                {"role": role, "value": value},
            )
        if not self._is_locally_bound(trigger, cleaned, text):
            raise VerificationError(
                f"Argument span {value!r} for role {role!r} is too far from the trigger.",
                "argument_not_locally_bound",
                {"role": role, "value": value},
            )
        if self._crosses_clause_boundary(trigger, cleaned, text):
            raise VerificationError(
                f"Argument span {value!r} for role {role!r} crosses a clause boundary with the trigger.",
                "argument_crosses_clause_boundary",
                {"role": role, "value": value},
            )
        if not self._matches_role_semantics(role, cleaned):
            raise VerificationError(
                f"Argument span {value!r} does not match the expected semantics for role {role!r}.",
                "argument_role_semantics",
                {"role": role, "value": value},
            )

    def _is_locally_bound(self, trigger: str, value: str, text: str, window: int = 260) -> bool:
        normalized_text = self._normalize_whitespace(text)
        trigger_idx = normalized_text.lower().find(self._normalize_whitespace(trigger).lower())
        value_idx = normalized_text.lower().find(value.lower())
        if trigger_idx == -1 or value_idx == -1:
            return False
        return abs(value_idx - trigger_idx) <= window

    def _crosses_clause_boundary(self, trigger: str, value: str, text: str) -> bool:
        normalized_text = self._normalize_whitespace(text)
        trigger_idx = normalized_text.lower().find(self._normalize_whitespace(trigger).lower())
        value_idx = normalized_text.lower().find(value.lower())
        if trigger_idx == -1 or value_idx == -1:
            return True
        start = min(trigger_idx, value_idx)
        end = max(trigger_idx, value_idx)
        between = normalized_text[start:end]
        return bool(self.CLAUSE_BOUNDARY_RE.search(between))

    def _matches_role_semantics(self, role: str, value: str) -> bool:
        role_key = role.lower().replace("-", "_")
        pattern = self.ROLE_SEMANTIC_HINTS.get(role_key)
        if not pattern:
            return True
        return bool(re.search(pattern, value, flags=re.IGNORECASE))

    def _normalize_whitespace(self, value: str) -> str:
        return " ".join(value.split())
