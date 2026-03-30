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
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a care task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Gather tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.schedule: list[Task] = []

    def generate_schedule(self) -> list[Task]:
        """Build an ordered daily schedule from all pets' tasks, respecting constraints."""
        priority_rank = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = sorted(
            all_tasks,
            key=lambda t: (priority_rank[t.priority], t.duration_minutes),
        )

        total_minutes = 0
        self.schedule = []
        for task in sorted_tasks:
            if total_minutes + task.duration_minutes <= self.owner.available_minutes:
                self.schedule.append(task)
                total_minutes += task.duration_minutes

        return self.schedule

    def get_explanation(self) -> str:
        """Return a human-readable explanation of why tasks were ordered this way."""
        if not self.schedule:
            return "No tasks scheduled."

        lines = [
            f"Schedule for {self.owner.name} "
            f"({self.owner.available_minutes} minutes available):",
            "",
            "Tasks are ordered by priority (high first), "
            "then by shortest duration within the same priority.",
            "",
        ]

        total = 0
        for i, task in enumerate(self.schedule, start=1):
            total += task.duration_minutes
            lines.append(
                f"  {i}. {task.title} for {task.pet_name} "
                f"- {task.duration_minutes} min ({task.priority.value} priority)"
            )

        lines.append("")
        lines.append(f"Total scheduled: {total} / {self.owner.available_minutes} minutes")

        skipped = [t for t in self.owner.get_all_tasks() if t not in self.schedule]
        if skipped:
            lines.append("")
            lines.append("Skipped (not enough time):")
            for task in skipped:
                lines.append(
                    f"  - {task.title} for {task.pet_name} "
                    f"- {task.duration_minutes} min ({task.priority.value} priority)"
                )

        return "\n".join(lines)
