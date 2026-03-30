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
whiskers.add_task(Task("Feeding", 10, Priority.HIGH, "Whiskers", time="07:00", frequency="daily"))
mochi.add_task(Task("Morning walk", 30, Priority.HIGH, "Mochi", time="08:00", frequency="daily"))
mochi.add_task(Task("Medication", 5, Priority.HIGH, "Mochi", time="09:00", frequency="weekly"))
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

# --- Sort by time (chronological) ---
print()
print("Sorted by time (chronological):")
print()
for task in scheduler.sort_by_time():
    print(f"  {task.time}  {task.description:<20} ({task.pet_name})")

# --- Filter by pet ---
print()
print("Mochi's tasks only:")
for task in scheduler.filter_by_pet("Mochi"):
    print(f"  {task.time}  {task.description} - {task.duration_minutes} min")

# --- Filter by status ---
mochi.tasks[0].mark_complete()
print()
print(f"Completed: {scheduler.filter_by_status(completed=True)[0].description}")
print(f"Incomplete tasks: {len(scheduler.filter_by_status(completed=False))}")

# --- Recurring tasks ---
print()
print("Recurring task demo:")
walk = mochi.tasks[1]  # Morning walk (daily)
print(f"  Completing '{walk.description}' (frequency: {walk.frequency}, due: {walk.due_date})")
next_walk = walk.mark_complete()
if next_walk:
    mochi.add_task(next_walk)
    print(f"  Next occurrence created: due {next_walk.due_date}")

meds = mochi.tasks[2]  # Medication (weekly)
print(f"  Completing '{meds.description}' (frequency: {meds.frequency}, due: {meds.due_date})")
next_meds = meds.mark_complete()
if next_meds:
    mochi.add_task(next_meds)
    print(f"  Next occurrence created: due {next_meds.due_date}")

grooming = mochi.tasks[0]  # Grooming (once)
print(f"  Completing '{grooming.description}' (frequency: {grooming.frequency}, due: {grooming.due_date})")
next_grooming = grooming.mark_complete()
if next_grooming:
    mochi.add_task(next_grooming)
    print(f"  Next occurrence created: due {next_grooming.due_date}")
else:
    print(f"  No next occurrence (one-time task)")
