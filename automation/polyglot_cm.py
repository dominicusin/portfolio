"""POLY-001 prototype: one resource, one owning manager, explicit conflicts."""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional


class ManagerConflict(RuntimeError):
    """A manager tried to own or change a resource owned by another manager."""


@dataclass
class Manager:
    name: str
    apply: Callable[[Any], Any]


@dataclass
class Resource:
    id: str
    kind: str
    spec: Dict[str, Any] = field(default_factory=dict)


class Fabric:
    """Minimal control plane where ownership is declared and enforced."""

    def __init__(self):
        self._managers: Dict[str, Manager] = {}
        self._owners: Dict[str, str] = {}
        self._applied: List[str] = []

    def register(self, manager: Manager) -> None:
        self._managers[manager.name] = manager

    def declare_owner(self, resource: Resource, manager_name: str) -> None:
        if manager_name not in self._managers:
            raise KeyError(f"unknown manager: {manager_name}")
        current = self._owners.get(resource.id)
        if current and current != manager_name:
            raise ManagerConflict(
                f"{resource.id} is owned by {current}, not {manager_name}")
        self._owners[resource.id] = manager_name

    def apply(self, resource: Resource, manager_name: str) -> Any:
        owner = self._owners.get(resource.id)
        if owner is None:
            raise ManagerConflict(f"{resource.id} has no declared owner")
        if owner != manager_name:
            raise ManagerConflict(f"{resource.id} belongs to {owner}")
        result = self._managers[manager_name].apply(resource)
        self._applied.append(resource.id)
        return result

    def conflicts(self, claims: Iterable[tuple]) -> List[str]:
        """Detect two managers claiming the same resource id."""
        seen: Dict[str, str] = {}
        out = []
        for resource_id, manager_name in claims:
            previous = seen.get(resource_id)
            if previous and previous != manager_name:
                out.append(f"{resource_id}: {previous} vs {manager_name}")
            else:
                seen[resource_id] = manager_name
        return out

    def applied(self) -> List[str]:
        return list(self._applied)
