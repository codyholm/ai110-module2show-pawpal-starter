import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant that schedules tasks by priority and time.")

# --- Session state: keep the Owner alive across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=60)

owner = st.session_state.owner

# --- Owner setup ---
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    new_name = st.text_input("Name", value=owner.name)
    if new_name != owner.name:
        owner.name = new_name
with col2:
    new_minutes = st.number_input(
        "Available minutes", min_value=1, max_value=480, value=owner.available_minutes
    )
    if new_minutes != owner.available_minutes:
        owner.available_minutes = new_minutes

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
        task_title = st.text_input("Task title", value="Morning walk")

    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.selectbox("Priority", ["high", "medium", "low"])

    if st.button("Add task"):
        selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=Priority(priority),
            pet_name=selected_pet_name,
        )
        selected_pet.add_task(task)

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.table([
            {
                "Pet": t.pet_name,
                "Task": t.title,
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority.value,
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

        if scheduler.schedule:
            st.table([
                {
                    "#": i,
                    "Task": t.title,
                    "Pet": t.pet_name,
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": t.priority.value,
                }
                for i, t in enumerate(scheduler.schedule, start=1)
            ])

        st.markdown(scheduler.get_explanation())
