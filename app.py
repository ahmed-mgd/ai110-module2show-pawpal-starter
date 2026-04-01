import streamlit as st
from datetime import datetime, time

from pawpal_system import Owner, Pet, RecurrenceType, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pets")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# Keep owner name aligned with the UI input while preserving all pets/tasks.
st.session_state.owner.name = owner_name

with st.form("add_pet_form", clear_on_submit=True):
    pet_col1, pet_col2, pet_col3 = st.columns([2, 1, 1])
    with pet_col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with pet_col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with pet_col3:
        pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=2)
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    clean_pet_name = pet_name.strip()
    if not clean_pet_name:
        st.error("Pet name is required.")
    else:
        try:
            st.session_state.owner.add_pet(
                Pet(name=clean_pet_name, species=species, age=int(pet_age))
            )
            st.success(f"Added pet: {clean_pet_name}")
        except ValueError as exc:
            st.error(str(exc))

if st.session_state.owner.pets:
    st.write("Current pets")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age}
            for pet in st.session_state.owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks to a selected pet using your backend classes.")

pet_options = [pet.name for pet in st.session_state.owner.pets]

with st.form("add_task_form", clear_on_submit=True):
    task_col1, task_col2, task_col3 = st.columns(3)
    with task_col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with task_col2:
        scheduled_at = st.time_input("Scheduled time", value=time(8, 0))
    with task_col3:
        recurrence = st.selectbox(
            "Recurrence",
            [
                RecurrenceType.NONE,
                RecurrenceType.DAILY,
                RecurrenceType.WEEKLY,
                RecurrenceType.MONTHLY,
            ],
            format_func=lambda r: r.value,
        )

    task_description = st.text_input("Task description", value="Walk around the block")
    selected_pet_name = st.selectbox(
        "Assign to pet",
        pet_options,
        index=0 if pet_options else None,
        placeholder="Add a pet first",
        disabled=not pet_options,
    )
    add_task_clicked = st.form_submit_button("Add task", disabled=not pet_options)

if add_task_clicked:
    clean_task_title = task_title.strip()
    clean_task_description = task_description.strip()
    if not clean_task_title:
        st.error("Task title is required.")
    elif not selected_pet_name:
        st.error("Add at least one pet before creating tasks.")
    else:
        selected_pet = st.session_state.owner.get_pet(selected_pet_name)
        task_dt = datetime.combine(datetime.now().date(), scheduled_at)
        task = Task(
            title=clean_task_title,
            description=clean_task_description,
            scheduled_time=task_dt,
            recurrence=recurrence,
        )
        selected_pet.add_task(task)
        st.success(f"Added task '{task.title}' for {selected_pet.name}")

all_tasks = [task for pet in st.session_state.owner.pets for task in pet.tasks]

if all_tasks:
    due_today_count = sum(1 for task in all_tasks if task.is_due_on(datetime.now().date()))
    m1, m2 = st.columns(2)
    m1.metric("Total tasks", len(all_tasks))
    m2.metric("Due today", due_today_count)

    st.write("Current tasks")
    st.table(
        [
            {
                "title": task.title,
                "pet": task.pet.name if task.pet else "",
                "time": task.scheduled_time.strftime("%H:%M"),
                "recurrence": task.recurrence.value,
                "completed": task.completed,
            }
            for task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button calls your Scheduler over today\'s tasks.")

generate_clicked = st.button("Generate schedule", disabled=not all_tasks)

if generate_clicked:
    scheduler = st.session_state.scheduler
    scheduler.tasks = []

    for pet in st.session_state.owner.pets:
        for task in pet.tasks:
            scheduler.add_task(task)

    today_tasks = scheduler.prioritize_tasks(datetime.now().date())
    if today_tasks:
        st.success("Today\'s Schedule")
        st.table(
            [
                {
                    "time": task.scheduled_time.strftime("%H:%M"),
                    "task": task.title,
                    "pet": task.pet.name if task.pet else "",
                    "recurrence": task.recurrence.value,
                }
                for task in today_tasks
            ]
        )
    else:
        st.info("No tasks due today.")
