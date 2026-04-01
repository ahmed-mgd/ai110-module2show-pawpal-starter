from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum


class RecurrenceType(Enum):
	NONE = "none"
	DAILY = "daily"
	WEEKLY = "weekly"
	MONTHLY = "monthly"


class TaskPriority(Enum):
	HIGH = "high"
	MEDIUM = "medium"
	LOW = "low"


@dataclass
class Task:
	title: str
	description: str
	scheduled_time: datetime
	duration_minutes: int = 30
	priority: TaskPriority = TaskPriority.MEDIUM
	recurrence: RecurrenceType = RecurrenceType.NONE
	completed: bool = False
	pet: Pet | None = field(default=None, repr=False)

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.completed = True

	def is_due_on(self, day: date) -> bool:
		"""Check if this task is due on a specific day, accounting for recurrence."""
		task_date = self.scheduled_time.date()
		if day < task_date:
			return False
		if self.recurrence == RecurrenceType.NONE:
			return day == task_date
		if self.recurrence == RecurrenceType.DAILY:
			return True
		if self.recurrence == RecurrenceType.WEEKLY:
			return day.weekday() == task_date.weekday()
		if self.recurrence == RecurrenceType.MONTHLY:
			return day.day == task_date.day
		return False

	def next_due_after(self, from_time: datetime) -> datetime:
		"""Calculate the next due time for this task after a given time."""
		if self.scheduled_time > from_time:
			return self.scheduled_time
		if self.recurrence == RecurrenceType.NONE:
			raise ValueError(f"Task '{self.title}' is not recurring and already passed")
		task_time = self.scheduled_time.time()
		candidate = datetime.combine(from_time.date(), task_time)
		if candidate <= from_time:
			candidate = datetime.combine(from_time.date() + timedelta(days=1), task_time)
		if self.recurrence == RecurrenceType.DAILY:
			return candidate
		if self.recurrence == RecurrenceType.WEEKLY:
			base_weekday = self.scheduled_time.weekday()
			days_ahead = (base_weekday - candidate.weekday()) % 7
			if days_ahead == 0:
				days_ahead = 0
			return candidate + timedelta(days=days_ahead)
		if self.recurrence == RecurrenceType.MONTHLY:
			target_day = self.scheduled_time.day
			if candidate.day >= target_day:
				if candidate.month == 12:
					candidate = candidate.replace(year=candidate.year + 1, month=1, day=1)
				else:
					candidate = candidate.replace(month=candidate.month + 1, day=1)
			try:
				candidate = candidate.replace(day=target_day)
			except ValueError:
				candidate = candidate.replace(day=28)
			return datetime.combine(candidate.date(), task_time)
		return candidate


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet."""
		task.pet = self
		self.tasks.append(task)

	def remove_task(self, task_title: str) -> None:
		"""Remove a task by title from this pet."""
		self.tasks = [t for t in self.tasks if t.title != task_title]

	def get_tasks_for_date(self, day: date) -> list[Task]:
		"""Get all incomplete tasks due on a specific day."""
		return [t for t in self.tasks if t.is_due_on(day) and not t.completed]


class Owner:
	def __init__(self, name: str, pets: list[Pet] | None = None) -> None:
		self.name = name
		self.pets = pets if pets is not None else []
		self._pets_by_name = {pet.name: pet for pet in self.pets}

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner's collection."""
		if pet.name in self._pets_by_name:
			raise ValueError(f"Pet '{pet.name}' already exists")
		self.pets.append(pet)
		self._pets_by_name[pet.name] = pet

	def remove_pet(self, pet_name: str) -> None:
		"""Remove a pet from this owner's collection."""
		if pet_name not in self._pets_by_name:
			raise ValueError(f"Pet '{pet_name}' not found")
		pet = self._pets_by_name.pop(pet_name)
		self.pets.remove(pet)

	def get_pet(self, pet_name: str) -> Pet:
		"""Retrieve a pet by name."""
		if pet_name not in self._pets_by_name:
			raise ValueError(f"Pet '{pet_name}' not found")
		return self._pets_by_name[pet_name]


class Scheduler:
	def __init__(self, tasks: list[Task] | None = None) -> None:
		self.tasks = tasks if tasks is not None else []

	def add_task(self, task: Task) -> None:
		"""Add a task to the scheduler."""
		if task not in self.tasks:
			self.tasks.append(task)

	def get_tasks_for_day(self, day: date) -> list[Task]:
		"""Get all incomplete tasks scheduled for a specific day."""
		return [t for t in self.tasks if t.is_due_on(day) and not t.completed]

	def get_tasks_for_pet(self, pet: Pet, day: date) -> list[Task]:
		"""Get all incomplete tasks for a specific pet on a specific day."""
		return [t for t in self.get_tasks_for_day(day) if t.pet is pet]

	def sort_by_time(self) -> list[Task]:
		"""Return all tasks sorted by scheduled_time (earliest first).

		Uses a lambda key on ``scheduled_time`` so that tasks added in any
		order are always presented chronologically.
		"""
		return sorted(self.tasks, key=lambda t: t.scheduled_time)

	def filter_by_status(self, completed: bool) -> list[Task]:
		"""Return tasks whose completion status matches *completed*.

		Args:
			completed: Pass ``True`` to get finished tasks, ``False`` for
				pending ones.
		"""
		return [t for t in self.tasks if t.completed == completed]

	def filter_by_pet_name(self, pet_name: str) -> list[Task]:
		"""Return tasks that belong to the pet with the given name.

		Args:
			pet_name: The exact name of the pet to filter by.
		"""
		return [t for t in self.tasks if t.pet is not None and t.pet.name == pet_name]

	def mark_task_complete(self, task: Task) -> Task | None:
		"""Mark *task* complete and, if it recurs, schedule the next occurrence.

		When a daily or weekly task is finished the method uses
		``task.next_due_after`` together with Python's ``timedelta`` to
		calculate the next due datetime and creates a fresh ``Task`` object
		with the same attributes.  The new task is registered with both the
		scheduler and the pet so the owner never has to re-enter it manually.

		Args:
			task: The task to complete.

		Returns:
			The newly created follow-up ``Task``, or ``None`` for one-time tasks.
		"""
		task.mark_complete()
		if task.recurrence == RecurrenceType.NONE:
			return None
		next_time = task.next_due_after(task.scheduled_time)
		new_task = Task(
			title=task.title,
			description=task.description,
			scheduled_time=next_time,
			duration_minutes=task.duration_minutes,
			priority=task.priority,
			recurrence=task.recurrence,
			completed=False,
			pet=task.pet,
		)
		self.add_task(new_task)
		if task.pet is not None:
			task.pet.tasks.append(new_task)
		return new_task

	def detect_conflicts(self) -> list[str]:
		"""Check all tasks for exact-time collisions and return warning strings.

		Two tasks conflict when they share the same ``scheduled_time``.  Rather
		than raising an exception the method collects every collision into a
		human-readable warning so the owner can decide how to resolve it.

		Returns:
			A list of warning strings (empty when there are no conflicts).
		"""
		warnings: list[str] = []
		seen: dict[datetime, Task] = {}
		for task in self.sort_by_time():
			if task.scheduled_time in seen:
				other = seen[task.scheduled_time]
				pet_a = task.pet.name if task.pet else "Unknown"
				pet_b = other.pet.name if other.pet else "Unknown"
				warnings.append(
					f"⚠️  Conflict at {task.scheduled_time.strftime('%Y-%m-%d %H:%M')}: "
					f"'{task.title}' ({pet_a}) overlaps with '{other.title}' ({pet_b})"
				)
			else:
				seen[task.scheduled_time] = task
		return warnings

	def prioritize_tasks(self, day: date) -> list[Task]:
		"""Get tasks for a day sorted by priority first, then time."""
		day_tasks = self.get_tasks_for_day(day)
		priority_rank = {
			TaskPriority.HIGH: 0,
			TaskPriority.MEDIUM: 1,
			TaskPriority.LOW: 2,
		}
		return sorted(day_tasks, key=lambda t: (priority_rank[t.priority], t.scheduled_time))
