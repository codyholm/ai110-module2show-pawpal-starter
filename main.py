"""CLI demo -- verify PawPal+ logic before connecting to Streamlit.

Run with: python main.py
"""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

# --- Setup ---
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="dog")
whiskers = Pet(name="Whiskers", species="cat")

owner.add_pet(mochi)
owner.add_pet(whiskers)

# Tasks added deliberately out of chronological order
mochi.add_task(Task("Grooming", 45, Priority.MEDIUM, "Mochi", time="14:00"))
whiskers.add_task(Task("Feeding", 10, Priority.HIGH, "Whiskers", time="07:00"))
mochi.add_task(Task("Morning walk", 30, Priority.HIGH, "Mochi", time="08:00"))
mochi.add_task(Task("Medication", 5, Priority.HIGH, "Mochi", time="09:00"))
whiskers.add_task(Task("Enrichment puzzle", 25, Priority.LOW, "Whiskers", time="16:00"))

# --- Generate and display schedule ---
scheduler = Scheduler(owner)
scheduler.generate_schedule()

print()
print(f"Today's Schedule for {owner.name}")
print("Priority first, then scheduled time.")
print()
print(f"  {'#':<4} {'Task':<20} {'Pet':<12} {'Time':>6}  {'Dur':>6}  Priority")
print(f"  {'--':<4} {'--------------------':<20} {'------------':<12} {'------':>6}  {'------':>6}  --------")

for i, task in enumerate(scheduler.schedule, start=1):
    print(
        f"  {f'{i}.':<4} {task.description:<20} {task.pet_name:<12} {task.time:>6}"
        f"  {task.duration_minutes:>4} min  {task.priority.value.upper()}"
    )
