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

print()
print(f"Today's Schedule for {owner.name} ({owner.available_minutes} min available)")
print("Priority first, then shortest duration.")
print()
print(f"  {'#':<4} {'Task':<20} {'Pet':<12} {'Time':>6}  Priority")
print(f"  {'--':<4} {'--------------------':<20} {'------------':<12} {'------':>6}  --------")

total = 0
for i, task in enumerate(scheduler.schedule, start=1):
    total += task.duration_minutes
    print(f"  {f'{i}.':<4} {task.title:<20} {task.pet_name:<12} {task.duration_minutes:>4} min  {task.priority.value.upper()}")

print(f"  {'':<4} {'':<20} {'':<12} {'------':>6}")
print(f"  {'':<4} {'':<20} {'Total:':>12} {total:>4} / {owner.available_minutes} min")

skipped = [t for t in owner.get_all_tasks() if t not in scheduler.schedule]
if skipped:
    print()
    print("  Skipped (not enough time):")
    for task in skipped:
        print(f"    - {task.title} ({task.pet_name}) - {task.duration_minutes} min, {task.priority.value}")
