"""PawPal+ logic layer -- class skeletons derived from UML (notes.md Step 3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: Priority
    pet_name: str
    time: str = "08:00"
    frequency: str = "once"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Task | None:
        """Mark this task as done. Returns the next occurrence if recurring."""
        self.completed = True
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None
        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            pet_name=self.pet_name,
            time=self.time,
            frequency=self.frequency,
            due_date=next_date,
        )


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
        """Build an ordered daily schedule, sorted by priority then scheduled time."""
        priority_rank = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        all_tasks = self.owner.get_all_tasks()
        self.schedule = sorted(
            all_tasks,
            key=lambda t: (priority_rank[t.priority], t.time),
        )
        return self.schedule

    def sort_by_time(self) -> list[Task]:
        """Sort all tasks chronologically by their scheduled time."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return only tasks belonging to the given pet."""
        return [t for t in self.owner.get_all_tasks() if t.pet_name == pet_name]

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the given completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self) -> list[str]:
        """Check for overlapping tasks and return warning messages."""
        tasks = self.sort_by_time()
        warnings = []
        for i in range(len(tasks)):
            # Calculate end time in minutes since midnight
            h1, m1 = map(int, tasks[i].time.split(":"))
            start1 = h1 * 60 + m1
            end1 = start1 + tasks[i].duration_minutes
            for j in range(i + 1, len(tasks)):
                h2, m2 = map(int, tasks[j].time.split(":"))
                start2 = h2 * 60 + m2
                # Since tasks are sorted by time, if start2 >= end1
                # then no further tasks can overlap with task i
                if start2 >= end1:
                    break
                warnings.append(
                    f"Conflict: '{tasks[i].description}' ({tasks[i].time}, "
                    f"{tasks[i].duration_minutes} min) overlaps with "
                    f"'{tasks[j].description}' ({tasks[j].time}, "
                    f"{tasks[j].duration_minutes} min)"
                )
        return warnings

    def get_explanation(self) -> str:
        """Return a human-readable explanation of why tasks were ordered this way."""
        if not self.schedule:
            return "No tasks scheduled."

        lines = [
            f"Schedule for {self.owner.name}:",
            "",
            "Tasks are ordered by priority (high first), "
            "then by scheduled time within the same priority.",
            "",
        ]

        for i, task in enumerate(self.schedule, start=1):
            lines.append(
                f"  {i}. {task.description} for {task.pet_name} "
                f"at {task.time} - {task.duration_minutes} min "
                f"({task.priority.value} priority)"
            )

        return "\n".join(lines)
