"""
Event schema definitions and utilities.

In AEC the target structure for event extraction is defined by an
*event schema* that enumerates the event type and a set of argument
roles together with their expected data types.  This module provides
a minimal representation for such schemas and a generic
``EventObject`` class based on Pydantic’s ``BaseModel`` that can be
instantiated dynamically by the coding agent.

The ``EventSchema`` class captures an event type name and a mapping
from role names to simple Python types (e.g. ``str`` for strings).
Although the paper treats argument roles as lists of values, we leave
the multiplicity open – if a role is optional or can be repeated
depends on the schema and is enforced at instantiation time via
pydantic validation.

Example
-------

>>> schema = EventSchema(
...     event_type="Protest",
...     roles={"Initiator": str, "Location": str}
... )
>>> event = EventObject(event_type="Protest", trigger="strike", arguments={
...     "Initiator": ["Union"], "Location": ["Paris"]
... })
>>> event.json()
'{"event_type": "Protest", "trigger": "strike", "arguments": {"Initiator": ["Union"], "Location": ["Paris"]}}'

Note that this generic ``EventObject`` does not fix the roles – all
roles are stored inside the ``arguments`` dictionary.  If stricter
schema enforcement is required it is straightforward to subclass
``EventObject`` and add typed attributes for each role.  The
``generate_pydantic_model`` method on ``EventSchema`` provides a way
to create such subclasses on the fly.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Tuple, Type, get_type_hints
from pydantic import BaseModel, ValidationError, create_model

class EventSchema:
    """Representation of a single event schema.

    Parameters
    ----------
    event_type : str
        The name of the event type (e.g. ``"Protest"``).
    roles : Mapping[str, Type]
        A mapping from argument role names to the expected Python type
        of the argument.  Most schemas use ``str`` to indicate that
        the argument value should be a string, but other types can be
        used as well (e.g. ``int`` for numeric fields).
    """

    def __init__(self, event_type: str, roles: Mapping[str, Type[Any]]) -> None:
        self.event_type = event_type
        self.roles: Dict[str, Type[Any]] = dict(roles)

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "EventSchema":
        """Construct an event schema from a plain dictionary.

        The dictionary must contain an ``"event_type"`` key and a
        ``"roles"`` key mapping role names to type names.  Supported
        type names are ``"str"``, ``"int"``, ``"float"`` and ``"bool"``.
        Any unrecognised type name defaults to ``str``.
        """
        event_type = d.get("event_type")
        if not isinstance(event_type, str):
            raise ValueError("'event_type' must be a string")
        raw_roles = d.get("roles")
        if not isinstance(raw_roles, Mapping):
            raise ValueError("'roles' must be a mapping from role names to type names")
        roles: Dict[str, Type[Any]] = {}
        for role_name, type_name in raw_roles.items():
            if isinstance(type_name, str):
                type_name = type_name.lower()
            else:
                raise ValueError(f"Type for role {role_name!r} must be a string")
            if type_name in ("str", "string"):
                roles[role_name] = str
            elif type_name in ("int", "integer"):
                roles[role_name] = int
            elif type_name == "float":
                roles[role_name] = float
            elif type_name in ("bool", "boolean"):
                roles[role_name] = bool
            else:
                # default to string for unrecognised types
                roles[role_name] = str
        return cls(event_type, roles)

    def generate_pydantic_model(self, model_name: Optional[str] = None) -> Type[BaseModel]:
        """Dynamically generate a Pydantic model enforcing this schema.

        Returns a subclass of ``BaseModel`` with fields ``event_type``,
        ``trigger`` and one attribute per argument role.  Each role field
        expects a list of values of the declared type.  The generated
        model also includes a convenience method ``to_event_object`` to
        convert an instance into the generic :class:`EventObject`.

        Parameters
        ----------
        model_name : str, optional
            Custom name for the generated model.  If omitted, the
            model name defaults to ``"{event_type}Event"``.
        """
        name = model_name or f"{self.event_type}Event"
        # Build fields: event_type (str), trigger (str), and arguments
        fields: Dict[str, Tuple[Any, ...]] = {
            "event_type": (str, ...),
            "trigger": (str, ...),
        }
        for role, typ in self.roles.items():
            # Each argument is a list of the declared type
            fields[role] = (List[typ], [])
        # Define a helper to convert to generic EventObject
        def to_event_object(self_: BaseModel) -> "EventObject":
            args: Dict[str, List[Any]] = {}
            for role_name in self.roles.keys():
                args[role_name] = getattr(self_, role_name)
            return EventObject(event_type=self_.event_type, trigger=self_.trigger, arguments=args)
        model = create_model(name, __base__=BaseModel, __module__=__name__, **fields)  # type: ignore[arg-type]
        # attach method and schema reference
        setattr(model, "to_event_object", to_event_object)
        setattr(model, "_schema", self)
        return model


class EventObject(BaseModel):
    """Generic event representation used across the AEC pipeline.

    Attributes
    ----------
    event_type : str
        Name of the event type.
    trigger : str
        Textual span from the input that evokes the event.
    arguments : Dict[str, List[str]]
        Mapping from role names to a list of argument values.  Roles
        absent from this dictionary are interpreted as empty.
    """

    event_type: str
    trigger: str
    arguments: Dict[str, List[str]]

    class Config:
        extra = "forbid"

    def pretty_print(self) -> str:
        """Return a human‑readable string representation of the event."""
        lines = [f"Event type: {self.event_type}", f"Trigger: {self.trigger}"]
        for role, values in self.arguments.items():
            if values:
                lines.append(f"  {role}: {', '.join(map(str, values))}")
        return "\n".join(lines)