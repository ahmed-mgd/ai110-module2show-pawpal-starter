# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

## Features

- Add and manage owner + pet information
- Add and edit tasks with time, duration, recurrence, and priority
- Build a daily plan sorted by priority and time
- Show conflict warnings when tasks overlap at the same start time
- Auto-create next occurrence for recurring tasks when completed
- Filter tasks by pet and completion status

## 📸 Demo

Replace `pawpal_demo.png` with your screenshot filename after you capture it.

<a href="/course_images/ai110/pawpal_demo.png" target="_blank"><img src='/course_images/ai110/pawpal_demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Smarter Scheduling

PawPal+ includes several algorithmic features that make the scheduler more useful for a real pet owner:

- **Sort by time** — `Scheduler.sort_by_time()` returns all tasks in chronological order using a `lambda` key on `scheduled_time`, so tasks added in any order are always presented clearly.
- **Filter by pet** — `Scheduler.filter_by_pet_name(name)` returns only the tasks belonging to a specific pet, making it easy to view one animal's daily agenda at a glance.
- **Filter by status** — `Scheduler.filter_by_status(completed)` separates pending tasks from finished ones, so completed items never clutter the active schedule.
- **Recurring task auto-renewal** — `Scheduler.mark_task_complete(task)` marks a task done and, for daily or weekly tasks, automatically creates the next occurrence using Python's `timedelta`. The owner never has to re-enter a routine task.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans the schedule for tasks with identical start times and returns human-readable warning strings rather than crashing the program, giving the owner a chance to reschedule.

## Testing PawPal+

Run the automated suite with:

```bash
python -m pytest
```

The tests cover both happy paths and edge cases for:

- Task completion state changes (`mark_complete`)
- Pet task management (adding/removing and date retrieval)
- Owner pet lookup and removal behavior
- Scheduler chronological sorting (`sort_by_time` and `prioritize_tasks`)
- Recurrence auto-renewal when completing daily tasks (`mark_task_complete`)
- Conflict detection for duplicate times (`detect_conflicts`)
- Edge cases such as empty schedules and missing-pet filters

Confidence Level: 4/5 stars

The suite verifies the core scheduling behaviors reliably, but additional overlap-based conflict checks (using duration windows) would further improve confidence.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
