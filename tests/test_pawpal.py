"""Tests for PawPal+ core logic."""

from datetime import date

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


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


# -- Sorting correctness ---------------------------------------------------


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task("Grooming", 45, Priority.MEDIUM, "Mochi", time="14:00"))
    pet.add_task(Task("Feeding", 10, Priority.HIGH, "Mochi", time="07:00"))
    pet.add_task(Task("Medication", 5, Priority.HIGH, "Mochi", time="09:30"))

    scheduler = Scheduler(owner)
    result = scheduler.sort_by_time()

    assert [t.time for t in result] == ["07:00", "09:30", "14:00"]


def test_generate_schedule_orders_by_priority_then_time():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task("Grooming", 45, Priority.MEDIUM, "Mochi", time="09:00"))
    pet.add_task(Task("Feeding", 10, Priority.HIGH, "Mochi", time="10:00"))
    pet.add_task(Task("Walk", 30, Priority.HIGH, "Mochi", time="07:00"))
    pet.add_task(Task("Play", 20, Priority.LOW, "Mochi", time="08:00"))

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    assert [t.description for t in scheduler.schedule] == [
        "Walk", "Feeding", "Grooming", "Play"
    ]


def test_sort_by_time_same_time_is_stable():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, Priority.HIGH, "Mochi", time="08:00"))
    pet.add_task(Task("Feeding", 10, Priority.HIGH, "Mochi", time="08:00"))

    scheduler = Scheduler(owner)
    result = scheduler.sort_by_time()

    assert len(result) == 2
    assert result[0].time == result[1].time == "08:00"
    # Python's stable sort preserves insertion order
    assert [t.description for t in result] == ["Walk", "Feeding"]


# -- Recurrence logic -------------------------------------------------------


def test_mark_complete_daily_creates_next_day_task():
    task = Task(
        "Morning walk", 30, Priority.HIGH, "Mochi",
        time="08:00", frequency="daily", due_date=date(2026, 3, 30),
    )
    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 3, 31)
    assert next_task.completed is False
    # All fields should carry over
    assert next_task.description == "Morning walk"
    assert next_task.duration_minutes == 30
    assert next_task.priority == Priority.HIGH
    assert next_task.pet_name == "Mochi"
    assert next_task.time == "08:00"
    assert next_task.frequency == "daily"


def test_mark_complete_weekly_creates_next_week_task():
    task = Task(
        "Medication", 5, Priority.HIGH, "Mochi",
        time="09:00", frequency="weekly", due_date=date(2026, 3, 30),
    )
    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == date(2026, 4, 6)
    assert next_task.frequency == "weekly"


def test_mark_complete_once_returns_none():
    task = Task("Vet visit", 60, Priority.HIGH, "Mochi", frequency="once")
    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is None


# -- Conflict detection -----------------------------------------------------


def test_detect_conflicts_finds_overlapping_tasks():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, Priority.HIGH, "Mochi", time="08:00"))
    pet.add_task(Task("Vet visit", 60, Priority.HIGH, "Mochi", time="08:15"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Vet visit" in warnings[0]


def test_detect_conflicts_no_overlap_returns_empty():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, Priority.HIGH, "Mochi", time="08:00"))
    pet.add_task(Task("Feeding", 10, Priority.HIGH, "Mochi", time="09:00"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 0


def test_detect_conflicts_adjacent_tasks_no_conflict():
    """Back-to-back tasks (end time == start time) should not conflict."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, Priority.HIGH, "Mochi", time="08:00"))
    pet.add_task(Task("Feeding", 15, Priority.HIGH, "Mochi", time="08:30"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 0


# -- Filtering --------------------------------------------------------------


def test_filter_by_pet_returns_only_matching_tasks():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    mochi.add_task(Task("Walk", 30, Priority.HIGH, "Mochi"))
    mochi.add_task(Task("Grooming", 45, Priority.MEDIUM, "Mochi"))
    whiskers.add_task(Task("Feeding", 10, Priority.HIGH, "Whiskers"))

    scheduler = Scheduler(owner)
    result = scheduler.filter_by_pet("Mochi")

    assert len(result) == 2
    assert all(t.pet_name == "Mochi" for t in result)


def test_filter_by_status_separates_complete_and_incomplete():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", 30, Priority.HIGH, "Mochi"))
    pet.add_task(Task("Feeding", 10, Priority.HIGH, "Mochi"))
    pet.tasks[0].mark_complete()

    scheduler = Scheduler(owner)
    done = scheduler.filter_by_status(completed=True)
    pending = scheduler.filter_by_status(completed=False)

    assert len(done) == 1
    assert done[0].completed is True
    assert len(pending) == 1
    assert pending[0].completed is False


# -- Aggregation / edge cases -----------------------------------------------


def test_get_all_tasks_aggregates_across_pets():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    mochi.add_task(Task("Walk", 30, Priority.HIGH, "Mochi"))
    mochi.add_task(Task("Grooming", 45, Priority.MEDIUM, "Mochi"))
    whiskers.add_task(Task("Feeding", 10, Priority.HIGH, "Whiskers"))

    assert len(owner.get_all_tasks()) == 3


def test_get_explanation_empty_schedule():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    assert scheduler.get_explanation() == "No tasks scheduled."
