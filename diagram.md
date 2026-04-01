```mermaid
classDiagram
    direction LR

    class Owner {
        +name: str
        +pets: list[Pet]
        +add_pet(pet: Pet)
        +remove_pet(pet_name: str)
        +get_pet(pet_name: str) Pet
    }

    class Pet {
        +name: str
        +species: str
        +age: int
        +tasks: list[Task]
        +add_task(task: Task)
        +remove_task(task_title: str)
        +get_tasks_for_date(day: date) list[Task]
    }

    class Task {
        +title: str
        +description: str
        +scheduled_time: datetime
        +recurrence: RecurrenceType
        +completed: bool
        +mark_complete()
        +is_due_on(day: date) bool
        +next_due_after(from_time: datetime) datetime
    }

    class Scheduler {
        +tasks: list[Task]
        +add_task(task: Task)
        +get_tasks_for_day(day: date) list[Task]
        +get_tasks_for_pet(pet: Pet, day: date) list[Task]
        +prioritize_tasks(day: date) list[Task]
    }

    class RecurrenceType {
        <<enumeration>>
        NONE
        DAILY
        WEEKLY
        MONTHLY
    }

    Owner "1" o-- "0..*" Pet : owns
    Pet "1" o-- "0..*" Task : has
    Task --> RecurrenceType : recurrence
    Scheduler "1" --> "0..*" Task : organizes
```