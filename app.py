import streamlit as st
from datetime import datetime, time

from pawpal_system import Owner, Pet, RecurrenceType, Scheduler, Task, TaskPriority

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

    extra_col1, extra_col2 = st.columns(2)
    with extra_col1:
        duration_minutes = st.number_input(
            "Duration (minutes)", min_value=5, max_value=480, value=30, step=5
        )
    with extra_col2:
        priority = st.selectbox(
            "Priority",
            [TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW],
            index=1,
            format_func=lambda p: p.value,
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
            duration_minutes=int(duration_minutes),
            priority=priority,
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
                "duration_min": task.duration_minutes,
                "priority": task.priority.value,
                "recurrence": task.recurrence.value,
                "completed": task.completed,
            }
            for task in all_tasks
        ]
    )

    st.markdown("#### Edit a Task")
    task_labels = [
        f"{task.pet.name if task.pet else 'Unknown'} | {task.title} | {task.scheduled_time.strftime('%H:%M')}"
        for task in all_tasks
    ]
    selected_task_label = st.selectbox("Select task to edit", task_labels)
    selected_task = all_tasks[task_labels.index(selected_task_label)]

    with st.form("edit_task_form"):
        edit_col1, edit_col2 = st.columns(2)
        with edit_col1:
            edit_title = st.text_input("Title", value=selected_task.title)
            edit_time = st.time_input("Time", value=selected_task.scheduled_time.time())
            edit_duration = st.number_input(
                "Duration (minutes)",
                min_value=5,
                max_value=480,
                value=selected_task.duration_minutes,
                step=5,
            )
        with edit_col2:
            edit_priority = st.selectbox(
                "Priority",
                [TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW],
                index=[TaskPriority.HIGH, TaskPriority.MEDIUM, TaskPriority.LOW].index(
                    selected_task.priority
                ),
                format_func=lambda p: p.value,
            )
            edit_recurrence = st.selectbox(
                "Recurrence",
                [
                    RecurrenceType.NONE,
                    RecurrenceType.DAILY,
                    RecurrenceType.WEEKLY,
                    RecurrenceType.MONTHLY,
                ],
                index=[
                    RecurrenceType.NONE,
                    RecurrenceType.DAILY,
                    RecurrenceType.WEEKLY,
                    RecurrenceType.MONTHLY,
                ].index(selected_task.recurrence),
                format_func=lambda r: r.value,
            )
            edit_completed = st.checkbox("Completed", value=selected_task.completed)

        edit_description = st.text_input("Description", value=selected_task.description)
        save_edit_clicked = st.form_submit_button("Save task edits")

    if save_edit_clicked:
        selected_task.title = edit_title.strip() or selected_task.title
        selected_task.description = edit_description.strip()
        selected_task.scheduled_time = datetime.combine(
            selected_task.scheduled_time.date(), edit_time
        )
        selected_task.duration_minutes = int(edit_duration)
        selected_task.priority = edit_priority
        selected_task.recurrence = edit_recurrence
        selected_task.completed = edit_completed
        st.success("Task updated.")
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

    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        st.warning("Schedule conflicts found. Please review these overlaps:")
        for warning in conflict_warnings:
            st.warning(warning)

    today_tasks = scheduler.prioritize_tasks(datetime.now().date())
    if today_tasks:
        st.success("Today\'s Schedule")
        st.table(
            [
                {
                    "time": task.scheduled_time.strftime("%H:%M"),
                    "task": task.title,
                    "pet": task.pet.name if task.pet else "",
                    "priority": task.priority.value,
                    "duration_min": task.duration_minutes,
                    "recurrence": task.recurrence.value,
                    "reason": (
                        f"{task.priority.value.title()} priority; scheduled at "
                        f"{task.scheduled_time.strftime('%H:%M')}"
                    ),
                }
                for task in today_tasks
            ]
        )
    else:
        st.info("No tasks due today.")
