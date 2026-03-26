"""PawPal+ logic layer -- class skeletons derived from UML (notes.md Step 3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    pet_name: str


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a care task to this pet."""
        ...


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        ...

    def get_all_tasks(self) -> list[Task]:
        """Gather tasks across all pets."""
        ...


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.schedule: list[Task] = []

    def generate_schedule(self) -> list[Task]:
        """Build an ordered daily schedule from all pets' tasks, respecting constraints."""
        ...

    def get_explanation(self) -> str:
        """Return a human-readable explanation of why tasks were ordered this way."""
        ...
