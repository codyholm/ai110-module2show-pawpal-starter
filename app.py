import os

import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

DATA_FILE = "data.json"

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant that schedules tasks by priority and time.")

# --- Session state: keep the Owner alive across reruns ---
if "owner" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.owner = Owner.load_from_json(DATA_FILE)
    else:
        st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# --- Owner setup ---
st.subheader("Owner")
new_name = st.text_input("Name", value=owner.name)
if new_name != owner.name:
    owner.name = new_name
    owner.save_to_json(DATA_FILE)

st.divider()

# --- Add a pet ---
st.subheader("Pets")

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    owner.save_to_json(DATA_FILE)
    st.session_state.pop("scheduler", None)

if owner.pets:
    for pet in owner.pets:
        task_count = len(pet.tasks)
        st.write(f"**{pet.name}** ({pet.species}) — {task_count} task{'s' if task_count != 1 else ''}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add tasks to a pet ---
st.subheader("Tasks")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    col1, col2 = st.columns(2)
    with col1:
        selected_pet_name = st.selectbox("Pet", pet_names)
    with col2:
        task_description = st.text_input("Description", value="Morning walk")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"])
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        task = Task(
            description=task_description,
            duration_minutes=int(duration),
            priority=Priority(priority),
            pet_name=selected_pet_name,
            time=task_time,
            frequency=frequency,
        )
        selected_pet.add_task(task)
        owner.save_to_json(DATA_FILE)
        st.session_state.pop("scheduler", None)
        st.rerun()

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.table([
            {
                "Pet": t.pet_name,
                "Task": t.description,
                "Time": t.time,
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority.value,
                "Frequency": t.frequency,
            }
            for t in all_tasks
        ])
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first, then you can add tasks.")

st.divider()

# --- Generate schedule ---
st.subheader("Schedule")

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("No tasks to schedule. Add some tasks first.")
    else:
        scheduler = Scheduler(owner)
        scheduler.generate_schedule()
        st.session_state.scheduler = scheduler

if "scheduler" in st.session_state:
    scheduler = st.session_state.scheduler

    # --- Sort / filter controls ---
    col1, col2 = st.columns(2)
    with col1:
        sort_mode = st.radio("Sort by", ["Priority", "Time"], horizontal=True)
    with col2:
        pet_names = [p.name for p in owner.pets]
        pet_filter = st.selectbox(
            "Filter by pet", ["All pets"] + pet_names, key="pet_filter",
        )

    if pet_filter != "All pets":
        tasks = scheduler.filter_by_pet(pet_filter)
    else:
        tasks = scheduler.owner.get_all_tasks()

    if sort_mode == "Time":
        tasks = sorted(tasks, key=lambda t: t.time)
    else:
        priority_rank = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        tasks = sorted(tasks, key=lambda t: (priority_rank[t.priority], t.time))

    # --- Schedule table ---
    if tasks:
        st.table([
            {
                "#": i,
                "Task": t.description,
                "Pet": t.pet_name,
                "Time": t.time,
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority.value,
                "Frequency": t.frequency,
            }
            for i, t in enumerate(tasks, start=1)
        ])
    else:
        st.info("No tasks match this filter.")

    # --- Conflict detection (always checks full schedule) ---
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts detected.")

    # --- Status summary ---
    done = scheduler.filter_by_status(completed=True)
    remaining = scheduler.filter_by_status(completed=False)
    st.info(f"{len(done)} completed, {len(remaining)} remaining")

    # --- Explanation ---
    st.markdown(scheduler.get_explanation())
