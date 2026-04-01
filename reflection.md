# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Here are some core actions that the user should be able to perform:

- Add and manage pets
- Schedule single or recurring tasks (e.g. appointments, feeding, walks)
- View and organize tasks for the day

Here are the classes we will include:

- `Owner` will store user information and allow users to create and/or assign themselves to pets. It will store the following attributes:
  - Name
  - Pets (ref)

- `Pet` will store information for a given pet and its tasks. Attributes include:
  - Name
  - Species
  - Age
  - Tasks (ref)

- `Task` will store information for tasks such as feedings, appointments, etc. Attributes include:
  - Title
  - Description
  - Pet
  - Scheduled time
  - Duration
  - Priority
  - Recurrence (e.g. daily, monthly, etc)
  - Completed (bool)

- `Scheduler` will handle the organization logic. Attributes include:
  - Tasks (ref)

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. One change I made was to add a relationship from `Task` to `Pet` to allow `Scheduler` to more easily filter tasks by pet.

I also applied an internal name index `pets_by_name` to avoid linear scans and reduce lookup time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers task time, priority, recurrence, completion status, and pet assignment.

I treated priority and time as the most important constraints because they directly affect what the owner should do first. I used priority first (high before medium before low), then sorted by time to keep the schedule easy to follow.

**b. Tradeoffs**

The conflict detector checks for exact datetime matches rather than overlapping time windows. This means two tasks that actually overlap can slip through undetected as long as their start times differ by even one minute.

This tradeoff is still reasonable for this version because the goal was to keep the logic lightweight and readable. It gives clear warnings for the most obvious conflicts without making the scheduling logic too complex too early.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools mostly for brainstorming and then had a back and forth to solidify and iterate on the classes.

The prompts that helped the most were prompts asking to identify bottlenecks in the code. Those prompts exposed limitations that were not picked up initially.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One time I did not accept an AI suggestion was when it suggested many unnecessary fields that were not relevant to this project, like user emails, first names, and last names.

I evaluated whether those components would actually be useful for PawPal+, and I verified my judgment by reprompting with my objection and checking whether the updated response stayed aligned with the project scope.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested core behaviors in the scheduler and data model:

- task completion status changes
- adding/removing tasks on pets
- owner pet lookup and removal
- sorting and prioritization order
- recurring task regeneration for daily tasks
- conflict detection for duplicate task times
- edge cases like empty schedules and unknown pet filters

These tests were important because they verify the most important scheduling behaviors and also catch regressions when refactoring.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident overall: 4 out of 5.

If I had more time, I would test more edge cases around monthly recurrence on dates like the 31st, conflict detection with overlapping durations (not just exact same times), and behavior across timezone/day boundary cases.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I think I did a good job brainstorming and iterating over the initial idea, which gave me a good starting foundation. I am most satisfied with how the class design stayed modular while still being practical to implement.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would read over the README more carefully at the start so I could avoid some refactors later. I would also plan the UI requirements earlier so the integration step is smoother.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One key takeaway is to work in steps and commit incrementally to make steady progress. It makes it easier to validate each part, recover from mistakes, and keep AI suggestions aligned with the current project scope.
