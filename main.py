"""CLI demo -- verify PawPal+ logic before connecting to Streamlit.

Run with: python main.py
"""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=60)

mochi = Pet(name="Mochi", species="dog")
whiskers = Pet(name="Whiskers", species="cat")

owner.add_pet(mochi)
owner.add_pet(whiskers)

# Total across all tasks: 115 min -- exceeds the 60-min budget on purpose
mochi.add_task(Task("Morning walk", 30, Priority.HIGH, "Mochi"))
mochi.add_task(Task("Medication", 5, Priority.HIGH, "Mochi"))
mochi.add_task(Task("Grooming", 45, Priority.MEDIUM, "Mochi"))
whiskers.add_task(Task("Feeding", 10, Priority.HIGH, "Whiskers"))
whiskers.add_task(Task("Enrichment puzzle", 25, Priority.LOW, "Whiskers"))

# --- Generate and display schedule ---
scheduler = Scheduler(owner)
scheduler.generate_schedule()

print("=" * 50)
print(f"  Today's Schedule for {owner.name}")
print(f"  Time budget: {owner.available_minutes} minutes")
print("=" * 50)

total = 0
for i, task in enumerate(scheduler.schedule, start=1):
    total += task.duration_minutes
    print(f"  {i}. [{task.priority.value.upper():6s}] {task.title:<20s} "
          f"({task.pet_name}) - {task.duration_minutes} min")

print("-" * 50)
print(f"  Total: {total} / {owner.available_minutes} minutes")

skipped = [t for t in owner.get_all_tasks() if t not in scheduler.schedule]
if skipped:
    print()
    print("  Skipped (not enough time):")
    for task in skipped:
        print(f"    - {task.title} ({task.pet_name}) - {task.duration_minutes} min")

print()
print(scheduler.get_explanation())
