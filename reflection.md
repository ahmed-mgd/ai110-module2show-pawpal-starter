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

**b. Tradeoffs**

The conflict detector checks for exact datetime matches rather than overlapping time windows. This means two tasks that actually overlap can slip through undetected as long as their start times differ by even one minute.

This tradeoff is not overly problematic for a first version because task durations are currently not stored, so there is no reliable way to calculate overlap. An exact-match check is simpler to implement, but we could iterate on this in the future.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
