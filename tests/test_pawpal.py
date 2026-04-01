import pytest
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler, RecurrenceType


class TestTask:
    """Tests for Task class."""

    def test_mark_complete(self):
        """Verify that mark_complete() changes task's completed status."""
        task = Task(
            title="Feed Dog",
            description="Give food",
            scheduled_time=datetime.now(),
        )
        assert task.completed is False
        task.mark_complete()
        assert task.completed is True

    def test_is_due_on_single_occurrence(self):
        """Verify is_due_on for non-recurring tasks."""
        today = date.today()
        task = Task(
            title="Vet Appointment",
            description="Check-up",
            scheduled_time=datetime.combine(today, datetime.min.time()),
            recurrence=RecurrenceType.NONE,
        )
        assert task.is_due_on(today) is True
        assert task.is_due_on(today + __import__('datetime').timedelta(days=1)) is False

    def test_is_due_on_daily_recurrence(self):
        """Verify is_due_on for daily recurring tasks."""
        today = date.today()
        task = Task(
            title="Morning Walk",
            description="Daily walk",
            scheduled_time=datetime.combine(today, datetime.min.time()),
            recurrence=RecurrenceType.DAILY,
        )
        assert task.is_due_on(today) is True
        assert task.is_due_on(today + __import__('datetime').timedelta(days=7)) is True


class TestPet:
    """Tests for Pet class."""

    def test_add_task_increases_count(self):
        """Verify that adding a task to a Pet increases task count."""
        pet = Pet(name="Buddy", species="Dog", age=3)
        assert len(pet.tasks) == 0

        task = Task(
            title="Walk",
            description="Evening walk",
            scheduled_time=datetime.now(),
        )
        pet.add_task(task)
        assert len(pet.tasks) == 1
        assert pet.tasks[0] == task

    def test_add_multiple_tasks(self):
        """Verify adding multiple tasks to a pet."""
        pet = Pet(name="Whiskers", species="Cat", age=2)
        tasks = [
            Task(
                title=f"Task {i}",
                description=f"Description {i}",
                scheduled_time=datetime.now(),
            )
            for i in range(3)
        ]

        for task in tasks:
            pet.add_task(task)

        assert len(pet.tasks) == 3

    def test_remove_task(self):
        """Verify that removing a task works correctly."""
        pet = Pet(name="Buddy", species="Dog", age=3)
        task = Task(
            title="Feed",
            description="Feeding time",
            scheduled_time=datetime.now(),
        )
        pet.add_task(task)
        assert len(pet.tasks) == 1

        pet.remove_task("Feed")
        assert len(pet.tasks) == 0

    def test_get_tasks_for_date(self):
        """Verify getting tasks for a specific date."""
        pet = Pet(name="Buddy", species="Dog", age=3)
        today = date.today()

        task_today = Task(
            title="Walk Today",
            description="Walk",
            scheduled_time=datetime.combine(today, datetime.min.time()),
            recurrence=RecurrenceType.NONE,
        )
        pet.add_task(task_today)

        tasks = pet.get_tasks_for_date(today)
        assert len(tasks) == 1
        assert tasks[0].title == "Walk Today"


class TestOwner:
    """Tests for Owner class."""

    def test_add_pet(self):
        """Verify that adding a pet to owner works."""
        owner = Owner("Alice")
        pet = Pet(name="Buddy", species="Dog", age=3)

        owner.add_pet(pet)
        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Buddy"

    def test_get_pet(self):
        """Verify retrieving a pet by name."""
        owner = Owner("Alice")
        pet = Pet(name="Buddy", species="Dog", age=3)
        owner.add_pet(pet)

        retrieved = owner.get_pet("Buddy")
        assert retrieved.name == "Buddy"
        assert retrieved is pet

    def test_get_pet_not_found(self):
        """Verify that getting non-existent pet raises error."""
        owner = Owner("Alice")
        with pytest.raises(ValueError, match="not found"):
            owner.get_pet("NonExistent")

    def test_remove_pet(self):
        """Verify removing a pet."""
        owner = Owner("Alice")
        pet = Pet(name="Buddy", species="Dog", age=3)
        owner.add_pet(pet)
        assert len(owner.pets) == 1

        owner.remove_pet("Buddy")
        assert len(owner.pets) == 0


class TestScheduler:
    """Tests for Scheduler class."""

    def test_add_task_to_scheduler(self):
        """Verify adding tasks to scheduler."""
        scheduler = Scheduler()
        task = Task(
            title="Walk",
            description="Walk",
            scheduled_time=datetime.now(),
        )
        scheduler.add_task(task)
        assert len(scheduler.tasks) == 1

    def test_get_tasks_for_day(self):
        """Verify getting tasks scheduled for a specific day."""
        scheduler = Scheduler()
        today = date.today()

        task1 = Task(
            title="Walk",
            description="Walk",
            scheduled_time=datetime.combine(today, datetime.min.time()),
            recurrence=RecurrenceType.DAILY,
        )
        task2 = Task(
            title="Future Task",
            description="Task",
            scheduled_time=datetime.combine(
                today + __import__('datetime').timedelta(days=1), datetime.min.time()
            ),
            recurrence=RecurrenceType.NONE,
        )

        scheduler.add_task(task1)
        scheduler.add_task(task2)

        today_tasks = scheduler.get_tasks_for_day(today)
        assert len(today_tasks) == 1
        assert today_tasks[0].title == "Walk"

    def test_prioritize_tasks(self):
        """Verify tasks are sorted by scheduled time."""
        scheduler = Scheduler()
        today = date.today()

        task1 = Task(
            title="Afternoon Task",
            description="Later",
            scheduled_time=datetime.combine(today, datetime.min.time().replace(hour=14)),
            recurrence=RecurrenceType.DAILY,
        )
        task2 = Task(
            title="Morning Task",
            description="Earlier",
            scheduled_time=datetime.combine(today, datetime.min.time().replace(hour=8)),
            recurrence=RecurrenceType.DAILY,
        )

        scheduler.add_task(task1)
        scheduler.add_task(task2)

        prioritized = scheduler.prioritize_tasks(today)
        assert prioritized[0].title == "Morning Task"
        assert prioritized[1].title == "Afternoon Task"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
