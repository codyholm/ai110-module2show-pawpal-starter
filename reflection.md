# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    Initial UML design included 4 classes and 1 enum. 
    Task is for an activity, contains title, duration, priority, and the pet it belongs to. Pet is for an animal under an owner's care which contains name, species, and a list of Tasks. Owner is for the human owners, it contains name, available minutes, and a list of Pets. 
    The scheduler is the main orchestrator for app. It takes an owner, gathers all tasks for their owned pets, and produces a daily plan within the owners budgeted available minutes.


**b. Design changes**

- Did your design change during implementation?
    Yes design had to change a couple times during implementation to make sure requirements were met.
- If yes, describe at least one change and why you made it
    A lot of the changes were made due to needing to meet requirements that were either misunderstood or implemented wrong at first. One example is how things were scheduled, instead of using time for scheduling the original design only had time duration of tasks. When we implementing sorting in phase 4 we had to first fix Task class so it included time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
    The scheduler considers priority first when sorting so the highest priority tasks are shown first. Then within the same priority it is sorted by scheduled time. Priority is the main sort key because a pet getting its medication will have higher priority than a walk. Within same priority level it then goes in time order.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    One tradeoff is because priority comes first, a low priority task at 07:00 by default would show below a high priority task at 12:00. An owner looking at their morning might miss something early because it's buried below higher priority tasks.

- Why is that tradeoff reasonable for this scenario?
    That tradeoff is reasonable because the owner can always switch views. By default it is sorted by priority then time, but user can toggle to sort by time first instead.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used claude for brainstorming and planning then implementing.
- What kinds of prompts or questions were most helpful?
    The ones where I had it explain how certain logic could work for the algorithmic layer when adding sorting, conflict detection, and more. Being specific with requests but asking discovery questions were the most helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    At first when designing and doing core implementation, AI misunderstood how scheduling should work. It built a time budget system, where each owner had a certain amount of time and every task would take a time duration. It would organize and try to fit tasks into the alloted time, instead of scheduling the tasks and looking for conflicts with overlapping tasks.
- How did you evaluate or verify what the AI suggested?
    When first planning I did not catch at first during evaluation of the diagram or implementation plan because the the logic was similar, but didn't actually fit the intent. Claude used same words like time and conflicts, but it wasn't until verifying the changes in app that we had to revisit.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    Behaviors we tested were sorting, recurrence, schedule conflicts, filtering, and aggregation by creating 15 tests.
- Why were these tests important?
    These were important because they tested the full logic and scope of app, such as making sure daily tasks are correctly set to reoccur and that the conflict detection works.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  I am very confident the core scheduling logic works correctly as it has been fully tested. There are however no tests for UI, input validation, or full end to end running of app. 
- What edge cases would you test next if you had more time?
    Edge cases to test would be for invalid time inputs, negative task durations, two tasks with same time & duration & priority. Also tests for UI directly instead of just the logic.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    Our classes we set up at the beginning, and the separation of logic from the Data classes and the Scheduler. Although some changes were made during implementation to correct mistakes, the bulk of it was in scheduler because of how we had our classes set up. Claude successfully helped me brainstorm the overall design of it, even though we had to do some iterations to make it correct.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  Probably improve the way overlapping tasks work with the scheduler. Integrate the priority system so if there are conflicting tasks it would show the higher priority one as the primary task, and show the lower priority as a complete when possible. If they have same priority call it out to user.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  Even if using AI to brainstorm and plan the design and create diagram, always test and verify the logic. It can use the right words if given them, but build the wrong thing if it doesn't understand the full intent. Time duration vs actual Time, when this project needed both, being the key example.
