"""Ontology loading utilities."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Dict, Mapping, Optional

try:
    from .event_schema import EventSchema
except ImportError:
    from event_schema import EventSchema


@dataclass
class OntologyManager:
    """Load and store event schemas for one or more datasets."""

    dataset_files: Mapping[str, str]
    _schemas: Dict[str, Dict[str, EventSchema]] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        self._schemas = {}
        for dataset, file_path in self.dataset_files.items():
            self._schemas[dataset.lower()] = self._load_schemas_from_file(file_path)

    def _load_schemas_from_file(self, file_path: str) -> Dict[str, EventSchema]:
        """Parse a Python or plain text file containing dataclass event definitions."""

        text = Path(file_path).read_text(encoding="utf-8")
        schemas: Dict[str, EventSchema] = {}
        try:
            tree = ast.parse(text, filename=file_path)
            for node in tree.body:
                if not isinstance(node, ast.ClassDef):
                    continue
                has_dataclass = any(
                    isinstance(dec, ast.Name) and dec.id == "dataclass"
                    or isinstance(dec, ast.Attribute) and dec.attr == "dataclass"
                    for dec in node.decorator_list
                )
                if not has_dataclass:
                    continue
                roles: Dict[str, type] = {}
                for stmt in node.body:
                    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                        role = stmt.target.id
                        if role != "mention":
                            roles[role] = list
                schemas[node.name] = EventSchema(node.name, roles)
            return schemas
        except SyntaxError:
            current_class: Optional[str] = None
            current_roles: Dict[str, type] = {}
            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or line.startswith("@dataclass"):
                    continue
                class_match = re.match(r"class\s+([A-Za-z0-9_]+)", line)
                if class_match:
                    if current_class is not None:
                        schemas[current_class] = EventSchema(current_class, current_roles)
                    current_class = class_match.group(1)
                    current_roles = {}
                    continue
                if current_class is None or ":" not in line:
                    continue
                role = line.split(":", 1)[0].strip().lstrip("*")
                if role and role != "mention":
                    current_roles[role] = list
            if current_class is not None:
                schemas[current_class] = EventSchema(current_class, current_roles)
            return schemas

    def get_schema(self, dataset: str, event_type: str) -> Optional[EventSchema]:
        """Return the schema for a given dataset and event type, if present."""

        return self._schemas.get(dataset.lower(), {}).get(event_type)

    def build_definitions(self, dataset: str) -> str:
        """Construct Python dataclass definitions for all event types in a dataset."""

        schemas = self._schemas.get(dataset.lower(), {})
        if not schemas:
            return ""
        lines = ["from dataclasses import dataclass", "from typing import List", ""]
        for schema in schemas.values():
            lines.extend(["@dataclass", f"class {schema.event_type}:", "    mention: str"])
            for role in schema.roles.keys():
                lines.append(f"    {role}: List")
            lines.append("")
        return "\n".join(lines)

    @classmethod
    def from_directory(cls, dir_path: str) -> "OntologyManager":
        """Construct an ``OntologyManager`` by scanning a directory for ontology files."""

        path = Path(dir_path)
        dataset_files = {file.stem.lower(): str(file) for file in path.glob("*.py")}
        return cls(dataset_files=dataset_files)
