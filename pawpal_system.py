from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum


class RecurrenceType(Enum):
	NONE = "none"
	DAILY = "daily"
	WEEKLY = "weekly"
	MONTHLY = "monthly"


@dataclass
class Task:
	title: str
	description: str
	scheduled_time: datetime
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

	def prioritize_tasks(self, day: date) -> list[Task]:
		"""Get tasks for a day sorted by scheduled time (earliest first)."""
		day_tasks = self.get_tasks_for_day(day)
		return sorted(day_tasks, key=lambda t: t.scheduled_time)
