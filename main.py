from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, RecurrenceType

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

    # Step 3: Create Tasks
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    # Buddy's tasks
    task1 = Task(
        title="Morning Walk",
        description="Walk around the park",
        scheduled_time=today.replace(hour=8, minute=0),
        recurrence=RecurrenceType.DAILY,
    )

    task2 = Task(
        title="Lunch Feeding",
        description="Feed Buddy his lunch",
        scheduled_time=today.replace(hour=12, minute=30),
        recurrence=RecurrenceType.DAILY,
    )

    # Whiskers' tasks
    task3 = Task(
        title="Vet Appointment",
        description="Annual check-up",
        scheduled_time=tomorrow.replace(hour=14, minute=0),
        recurrence=RecurrenceType.NONE,
    )

    task4 = Task(
        title="Playtime",
        description="Interactive toy session",
        scheduled_time=today.replace(hour=18, minute=0),
        recurrence=RecurrenceType.WEEKLY,
    )

    # Add tasks to pets
    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)
    cat.add_task(task4)
    print(f"✅ Tasks created: {len(dog.tasks) + len(cat.tasks)} total tasks")

    # Step 4: Create Scheduler and add tasks
    scheduler = Scheduler()
    for task in dog.tasks + cat.tasks:
        scheduler.add_task(task)
    print(f"✅ Scheduler loaded: {len(scheduler.tasks)} tasks")

    # Step 5: Display Today's Schedule
    today_date = today.date()
    today_tasks = scheduler.get_tasks_for_day(today_date)
    print_schedule(f"Today's Schedule ({today_date})", today_tasks)

    # Step 6: Display Prioritized Tasks
    prioritized = scheduler.prioritize_tasks(today_date)
    print_schedule("Prioritized Order (sorted by time)", prioritized)

    # Step 7: Display Tasks by Pet
    buddy_today = scheduler.get_tasks_for_pet(dog, today_date)
    print_schedule(f"Buddy's Tasks for Today", buddy_today)

    whiskers_today = scheduler.get_tasks_for_pet(cat, today_date)
    print_schedule(f"Whiskers' Tasks for Today", whiskers_today)

    # Step 8: Test task completion
    print("\n✅ Testing Task Completion")
    print(f"  Before: task1.completed = {task1.completed}")
    task1.mark_complete()
    print(f"  After:  task1.completed = {task1.completed}")

    # Step 9: Show remaining tasks after completion
    remaining = scheduler.get_tasks_for_day(today_date)
    print_schedule("Remaining Tasks (completed tasks hidden)", remaining)

    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
