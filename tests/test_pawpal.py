"""Tests for PawPal+ core logic."""

from pawpal_system import Pet, Priority, Task


def test_mark_complete_changes_status():
    task = Task("Morning walk", 30, Priority.HIGH, "Mochi")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feeding", 10, Priority.HIGH, "Mochi"))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Grooming", 45, Priority.MEDIUM, "Mochi"))
    assert len(pet.tasks) == 2
