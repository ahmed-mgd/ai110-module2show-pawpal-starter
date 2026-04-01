from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
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

	def mark_complete(self) -> None:
		pass

	def is_due_on(self, day: date) -> bool:
		pass

	def next_due_after(self, from_time: datetime) -> datetime:
		pass


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def remove_task(self, task_title: str) -> None:
		pass

	def get_tasks_for_date(self, day: date) -> list[Task]:
		pass


class Owner:
	def __init__(self, name: str, pets: list[Pet] | None = None) -> None:
		self.name = name
		self.pets = pets if pets is not None else []

	def add_pet(self, pet: Pet) -> None:
		pass

	def remove_pet(self, pet_name: str) -> None:
		pass

	def get_pet(self, pet_name: str) -> Pet:
		pass


class Scheduler:
	def __init__(self, tasks: list[Task] | None = None) -> None:
		self.tasks = tasks if tasks is not None else []

	def add_task(self, task: Task) -> None:
		pass

	def get_tasks_for_day(self, day: date) -> list[Task]:
		pass

	def get_tasks_for_pet(self, pet: Pet, day: date) -> list[Task]:
		pass

	def prioritize_tasks(self, day: date) -> list[Task]:
		pass
