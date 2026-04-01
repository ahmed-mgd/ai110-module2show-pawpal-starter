from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, RecurrenceType, Scheduler, Task


def print_schedule(title: str, tasks: list[Task]) -> None:
    """Pretty-print a list of tasks."""
    print(f"\n📋 {title}")
    print("=" * 60)
    if not tasks:
        print("  No tasks scheduled.")
        return
    for i, task in enumerate(tasks, 1):
        status = "✓" if task.completed else "○"
        pet_info = f" ({task.pet.name})" if task.pet else ""
        print(
            f"  {i}. [{status}] {task.title}{pet_info}"
            f"\n     ⏰ {task.scheduled_time.strftime('%H:%M')}"
            f" | 🔁 {task.recurrence.value}"
            f"\n     📝 {task.description}"
        )


def main():
    """Main demo: create owner, pets, tasks, and schedule."""
    print("\nPawPal+ System Demo\n")

    # Step 1: Create an Owner
    owner = Owner("Alice")
    print(f"✅ Owner created: {owner.name}")

    # Step 2: Create Pets
    dog = Pet(name="Buddy", species="Golden Retriever", age=3)
    cat = Pet(name="Whiskers", species="Tabby Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"✅ Pets added: {[p.name for p in owner.pets]}")

    # Step 3: Create Tasks (intentionally out of order to demo sorting)
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    # Buddy's tasks — added out of chronological order on purpose
    task_walk = Task(
        title="Morning Walk",
        description="Walk around the park",
        scheduled_time=today.replace(hour=8, minute=0, second=0, microsecond=0),
        recurrence=RecurrenceType.DAILY,
    )
    task_lunch = Task(
        title="Lunch Feeding",
        description="Feed Buddy his lunch",
        scheduled_time=today.replace(hour=12, minute=30, second=0, microsecond=0),
        recurrence=RecurrenceType.DAILY,
    )
    task_evening_walk = Task(
        title="Evening Walk",
        description="Sunset stroll",
        scheduled_time=today.replace(hour=18, minute=0, second=0, microsecond=0),
        recurrence=RecurrenceType.DAILY,
    )

    # Whiskers' tasks
    task_vet = Task(
        title="Vet Appointment",
        description="Annual check-up",
        scheduled_time=tomorrow.replace(hour=14, minute=0, second=0, microsecond=0),
        recurrence=RecurrenceType.NONE,
    )
    task_play = Task(
        title="Playtime",
        description="Interactive toy session",
        scheduled_time=today.replace(hour=18, minute=0, second=0, microsecond=0),
        recurrence=RecurrenceType.WEEKLY,
    )
    task_grooming = Task(
        title="Grooming",
        description="Brush fur and trim nails",
        scheduled_time=today.replace(hour=10, minute=0, second=0, microsecond=0),
        recurrence=RecurrenceType.WEEKLY,
    )

    # Add tasks to pets
    dog.add_task(task_walk)
    dog.add_task(task_lunch)
    dog.add_task(task_evening_walk)
    cat.add_task(task_vet)
    cat.add_task(task_play)
    cat.add_task(task_grooming)
    total = len(dog.tasks) + len(cat.tasks)
    print(f"✅ Tasks created: {total} total tasks")

    # Step 4: Create Scheduler and add tasks
    scheduler = Scheduler()
    for task in dog.tasks + cat.tasks:
        scheduler.add_task(task)
    print(f"✅ Scheduler loaded: {len(scheduler.tasks)} tasks")

    # ------------------------------------------------------------------ #
    # DEMO: Sorting                                                        #
    # ------------------------------------------------------------------ #
    sorted_all = scheduler.sort_by_time()
    print_schedule("All Tasks — Sorted by Time (sort_by_time)", sorted_all)

    # ------------------------------------------------------------------ #
    # DEMO: Filtering by pet name                                          #
    # ------------------------------------------------------------------ #
    buddy_tasks = scheduler.filter_by_pet_name("Buddy")
    print_schedule("Filtered — Buddy's Tasks (filter_by_pet_name)", buddy_tasks)

    whiskers_tasks = scheduler.filter_by_pet_name("Whiskers")
    print_schedule("Filtered — Whiskers' Tasks (filter_by_pet_name)", whiskers_tasks)

    # ------------------------------------------------------------------ #
    # DEMO: Filtering by completion status                                 #
    # ------------------------------------------------------------------ #
    pending = scheduler.filter_by_status(completed=False)
    print_schedule("Filtered — Pending Tasks (filter_by_status=False)", pending)

    # ------------------------------------------------------------------ #
    # DEMO: Conflict detection                                             #
    # ------------------------------------------------------------------ #
    print("\n\n🔍 Conflict Detection")
    print("=" * 60)
    # task_evening_walk (Buddy, 18:00) and task_play (Whiskers, 18:00) collide
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")

    # ------------------------------------------------------------------ #
    # DEMO: Today's prioritised schedule                                   #
    # ------------------------------------------------------------------ #
    today_date = today.date()
    prioritized = scheduler.prioritize_tasks(today_date)
    print_schedule(f"Today's Prioritised Schedule ({today_date})", prioritized)

    # ------------------------------------------------------------------ #
    # DEMO: Recurring task auto-renewal                                    #
    # ------------------------------------------------------------------ #
    print("\n\n🔁 Recurring Task Completion Demo")
    print("=" * 60)
    print(f"  Completing '{task_walk.title}' (daily)...")
    new_walk = scheduler.mark_task_complete(task_walk)
    print(f"  task_walk.completed  = {task_walk.completed}")
    if new_walk:
        print(
            f"  Next occurrence created: '{new_walk.title}'"
            f" at {new_walk.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
        )

    # Show pending tasks after completion — completed walk is now hidden
    remaining = scheduler.filter_by_status(completed=False)
    print_schedule("Remaining Pending Tasks (after completing Morning Walk)", remaining)

    # ------------------------------------------------------------------ #
    # DEMO: Filtering completed tasks                                      #
    # ------------------------------------------------------------------ #
    done = scheduler.filter_by_status(completed=True)
    print_schedule("Completed Tasks (filter_by_status=True)", done)

    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
