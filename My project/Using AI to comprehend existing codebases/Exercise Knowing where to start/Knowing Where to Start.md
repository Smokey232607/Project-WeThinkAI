# Exercise: Knowing Where to Start
## Python

---

##  Simple Explanation

> Imagine you just walked into a toy factory and you don't know where anything is. This exercise is like using a friendly robot (AI) to help you figure out: Where are the toys? (Project Structure) How do we build new toys? (Feature Location) What are the toys made of? (Domain Model) And how would we fix a broken toy? (Practical Application)

---

## Part 1: Understanding Project Structure

###  Initial Exploration (Before AI Prompt)

So I cloned the repo and opened the folder. Here's what I saw:

```
python/TaskManager/
├── cli.py
├── task_manager.py
├── models.py
├── storage.py
└── tests/
    ├── test_task.py
    └── test_task_manager.py
```

My first guesses were:
- `cli.py` = probably where the user types commands
- `task_manager.py` = probably the "brain" that decides what happens when you create or delete a task
- `models.py` = probably describes what a "task" looks like (like a blueprint)
- `storage.py` = probably saves tasks to a file so they don't disappear when you close the app
- `tests/` = these check if the code works correctly

I looked for config files like `requirements.txt` or `package.json` but **couldn't find any**. That was weird at first. I thought every Python project needed a `requirements.txt`. 

Turns out this project uses **only Python's built-in tools** (standard library). No extra downloads needed! The README says Python 3.11+ is all you need.

**Technologies I identified:**
- Python 3.11+
- `argparse` (for command-line commands)
- `json` (for saving data)
- `datetime` (for dates)
- `uuid` (for making unique IDs)
- `enum` (for categories like priority levels)
- `unittest` (for testing)

###  AI Prompt I Used

> "I just joined a team maintaining a Python Task Manager CLI app. The folder has cli.py, task_manager.py, models.py, storage.py, and tests/. There are no requirements.txt or external dependencies. Can you explain the likely architecture, entry points, and how data flows through these files?"

###  AI Analysis vs. My Observations

| My Guess | AI Confirmation | Match? |
|----------|----------------|--------|
| cli.py handles user input |  Yes — it's the presentation layer |  Correct |
| task_manager.py is the "brain" |  Yes — business logic layer |  Correct |
| models.py is blueprints |  Yes — domain/entity layer |  Correct |
| storage.py saves to file |  Yes — data persistence layer |  Correct |
| Needs external libraries |  No — uses only standard library |  I was wrong! |

**Misconceptions I had:**
1. I assumed there would be a `requirements.txt` or some config file. There isn't one — the project is intentionally simple.
2. I thought the storage might use SQLite. It actually uses a plain JSON file (`tasks.json`).

**Important Entry Points:**
- **Run the app:** `python cli.py`
- **Run tests:** `python -m unittest discover tests`
- **Data file:** `tasks.json` (created automatically)

**Architectural Pattern:**
**Layered Architecture** (like a sandwich):
1.  **Top bread:** `cli.py` — talks to the user
2.  **Lettuce:** `task_manager.py` — makes decisions
3.  **Cheese:** `models.py` — defines what a task looks like
4.  **Bottom bread:** `storage.py` — saves to disk

---

## Part 2: Finding Feature Implementation (Task Export to CSV)

### 🔍 Initial Search

My team lead wants "Task Export to CSV." I need to find similar features first so I know where to add it.

**Search terms I used:**
1. `export` → **0 results** (no export feature exists)
2. `csv` → **0 results**
3. `file` → Found in `storage.py` (opens `tasks.json`)
4. `open(` → Found in `storage.py` only
5. `print` / `format` → Found `format_task()` in `cli.py`

**Files found related to file operations:**
- `storage.py` — has `load()` and `save()` methods that read/write JSON
- `cli.py` — has `format_task()` that turns a task into a pretty string for the screen

###  My Hypothesis

Since there is NO existing export feature, I had to guess where it should go based on patterns I saw:

**Where it should live:**
1. `cli.py` → Add a new command like `python cli.py export --filename tasks.csv`
2. `task_manager.py` → Add a method like `export_tasks_to_csv(filename)` that gets all tasks and formats them as CSV rows
3. Python has a built-in `csv` module (no extra install needed!)

**Related components to modify:**
- `cli.py` — new subparser for `export`
- `task_manager.py` — new business logic method
- `tests/` — new test cases for export

###  AI Prompt I Used

> "I need to add a 'Task Export to CSV' feature to this Task Manager. I searched for 'export' and 'csv' and found nothing. The only file operations are in storage.py (JSON load/save) and cli.py has a format_task() function. Where should I implement this feature, and what existing patterns should I follow?"

###  AI Guidance

**Where to implement:**
1. **CLI Layer (`cli.py`):** Add `export` subcommand with `--filename` argument
2. **Business Layer (`task_manager.py`):** Add `export_to_csv(filepath)` method
3. **Reuse existing:** Call `self.storage.get_all_tasks()` to get data, then use Python's `csv` module to write

**My plan for implementation:**
```
1. Add `import csv` to task_manager.py
2. Add `export_to_csv(self, filepath)` method:
   - Get all tasks via `self.storage.get_all_tasks()`
   - Open file with `csv.writer()`
   - Write header row: ID, Title, Description, Priority, Status, Due Date, Tags
   - Write one row per task
3. Add `export` command in cli.py:
   - subparser.add_parser("export")
   - argument for `--filename`
   - Call `task_manager.export_to_csv(args.filename)`
4. Add tests in `tests/test_task_manager.py`
```

---

## Part 3: Understanding Domain Model

###  Extracting the Domain Model

**Core entities I found in `models.py`:**

| Entity | What It Is |
|--------|-----------|
| `Task` | The main thing — a to-do item |
| `TaskStatus` | Where the task is in its life: `todo`, `in_progress`, `review`, `done` |
| `TaskPriority` | How important: `LOW(1)`, `MEDIUM(2)`, `HIGH(3)`, `URGENT(4)` |

**What a `Task` looks like (its attributes):**
```
Task
├── id: unique code (like "abc-123-xyz")
├── title: name of the task
├── description: more details
├── priority: LOW, MEDIUM, HIGH, or URGENT
├── status: todo, in_progress, review, or done
├── created_at: when it was born
├── updated_at: last time it changed
├── due_date: deadline (optional)
├── completed_at: when finished (optional)
└── tags: list of labels like ["work", "urgent"]
```

**Business logic I found:**
- `update(**kwargs)` — changes fields and updates the `updated_at` timestamp
- `mark_as_done()` — sets status to `DONE` and records `completed_at` time
- `is_overdue()` — returns `True` if `due_date` is in the past AND status is not `DONE`

###  My Initial Understanding (Diagram)

```
┌─────────────┐
│    Task     │
├─────────────┤
│  + title    │
│  + status   │◄────── todo → in_progress → review → done
│  + priority │◄────── LOW → MEDIUM → HIGH → URGENT
│  + due_date │
│  + tags[]   │
└─────────────┘
```

**What I think each entity represents:**
- **Task:** A single job or to-do item that needs tracking
- **Status:** The workflow stage (like an assembly line)
- **Priority:** How loudly the task is screaming for attention
- **Tags:** Sticky notes to group similar tasks together

**Questions I had:**
1. Can a task go backwards in status? (e.g., from `done` back to `todo`?) — The code doesn't prevent it.
2. What happens if two tasks have the same title? — That's fine; they have unique IDs.
3. Is there a limit to tags? — No limit in the code.

###  AI Prompt I Used

> "I'm trying to understand the Task Manager domain model. I found Task, TaskStatus (todo, in_progress, review, done), and TaskPriority (LOW=1, MEDIUM=2, HIGH=3, URGENT=4). A Task has title, description, dates, tags, and methods like mark_as_done() and is_overdue(). Can you explain how these entities relate, test my understanding with questions, and help me create a glossary?"

###  AI Questions & My Answers

**Q1:** *If a task is marked as DONE, can it still be overdue?*  
**My answer:** No! Because `is_overdue()` checks `status != TaskStatus.DONE`. Once done, it's never overdue.

**Q2:** *What happens when you change priority from LOW to URGENT?*  
**My answer:** The `update()` method changes `priority` and updates `updated_at`. Nothing else special happens.

**Q3:** *Can a task have no due date?*  
**My answer:** Yes! `due_date` is optional. If it's `None`, `is_overdue()` returns `False`.

**Q4:** *What's the difference between `updated_at` and `completed_at`?*  
**My answer:** `updated_at` changes on ANY edit. `completed_at` only gets set when status becomes `DONE`.

###  Domain Glossary

| Term | Definition |
|------|-----------|
| **Task** | A single to-do item with title, description, priority, status, and dates |
| **Status** | The current stage in the task lifecycle (todo → in_progress → review → done) |
| **Priority** | The urgency level (1=LOW, 2=MEDIUM, 3=HIGH, 4=URGENT) |
| **Overdue** | A task whose due date has passed and is not yet marked DONE |
| **Tag** | A label string used to categorize or group tasks |
| **Domain Model** | The blueprint that defines what "tasks" are and how they behave |

---

## Part 4: Practical Application

###  The Scenario

> **New Business Rule:** *"Tasks that are overdue for more than 7 days should be automatically marked as abandoned unless they are marked as high priority."*

###  What I Need to Know First

**Problem:** There is **NO "abandoned" status** in the current code! The `TaskStatus` enum only has:
- `TODO = "todo"`
- `IN_PROGRESS = "in_progress"`
- `REVIEW = "review"`
- `DONE = "done"`

So I need to **add** a new status first.

###  Planning: Files to Modify

| File | What to Change |
|------|---------------|
| `models.py` | Add `ABANDONED = "abandoned"` to `TaskStatus` enum |
| `task_manager.py` | Add `mark_overdue_as_abandoned()` method |
| `cli.py` | Add a command to trigger this (or run automatically) |
| `tests/test_task_manager.py` | Add tests for the new rule |

###  Outline of Changes

**1. In `models.py` — Add the new status:**
```python
class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    ABANDONED = "abandoned"  # <-- NEW
```

**2. In `task_manager.py` — Add the business rule:**
```python
from datetime import datetime, timedelta

def mark_overdue_as_abandoned(self):
    tasks = self.storage.get_all_tasks()
    seven_days_ago = datetime.now() - timedelta(days=7)

    for task in tasks:
        if (task.due_date and 
            task.due_date < seven_days_ago and 
            task.status != TaskStatus.DONE and
            task.priority != TaskPriority.HIGH):

            task.status = TaskStatus.ABANDONED
            task.updated_at = datetime.now()

    self.storage.save()
    return True
```

**3. In `cli.py` — Add a command:**
```python
# Add new subparser
abandon_parser = subparsers.add_parser("abandon-old", help="Mark very overdue tasks as abandoned")

# In the main if-elif block:
elif args.command == "abandon-old":
    task_manager.mark_overdue_as_abandoned()
    print("Marked overdue tasks as abandoned (except high priority).")
```

###  Questions I'd Ask My Team Before Implementing

1. **Should "abandoned" tasks still show up in normal `list` commands?** Or should they be hidden?
2. **Should URGENT tasks also be exempt?** The rule says "high priority" but URGENT (4) is higher than HIGH (3).
3. **Should this run automatically** (e.g., every time you open the app) or only when manually triggered?
4. **Should we notify the user** when tasks are auto-abandoned?
5. **Can a user "un-abandon" a task?** Should it go back to `todo`?

###  Reflection

**How did AI prompts help?**
- The AI confirmed my hypothesis about where to add the new status (in `models.py`)
- It helped me see that the `is_overdue()` method already has "overdue" logic, but I needed to extend it with a "7 days" threshold
- It pointed out that I should reuse `self.storage.get_all_tasks()` and `self.storage.save()` — the same pattern used everywhere else

**What am I still unsure about?**
- Whether the team wants this as a manual command or automatic background job
- If "abandoned" should be treated as "done" for statistics (the `get_statistics()` method counts by status)
- Whether the `is_overdue()` method should also consider "abandoned" tasks

**Next steps to deepen understanding:**
1. Run the existing tests to make sure I understand the test patterns
2. Ask the team about the 5 questions above
3. Check if JavaScript/Java versions have similar features for consistency

---

## Final Discussion and Reflection

###  My Approach to Understanding the Codebase

1. **Looked at the folder first** — like peeking into drawers before opening them
2. **Read the README** — got the "big picture" of what the app does
3. **Found the main entry point** (`cli.py`) — this is where the story starts
4. **Followed the data flow** — user types command → cli parses it → task_manager decides → storage saves → models define the shape
5. **Used AI to confirm guesses** — instead of staying confused, I asked "Am I right about...?"

###  Personal Reflection

**Which prompt was most helpful?**  
The **"Understanding Project Structure"** prompt was the most helpful because it gave me the "map" of the codebase. Once I knew the layers (CLI → Manager → Storage → Models), everything else became easier to find.

**What would I do differently next time?**  
- I would run the app first (create a task, list it) to see it working before reading code
- I would draw the data flow diagram on paper before asking AI
- I would check the tests earlier — they show expected behavior clearly

**Additional tools that would help:**  
- A visual diagram generator (like drawing the class relationships)
- A debugger to step through the code line-by-line
- The `tree` command to see the folder structure faster

---

#  SUBMISSION SUMMARY (1-2 Pages)

## Initial vs. Final Understanding of the Task Manager Codebase

| Aspect | Initial Understanding | Final Understanding |
|--------|----------------------|---------------------|
| **Dependencies** | Thought it needed external libraries | Uses **only Python standard library** — no installs needed |
| **Architecture** | Guessed it was a simple script | It's a **layered architecture**: CLI → Business Logic → Storage → Models |
| **Data Storage** | Assumed SQLite or database | Plain **JSON file** (`tasks.json`) with custom encoder/decoder |
| **Entry Point** | Knew `cli.py` was important | `cli.py` is the **presentation layer**; `task_manager.py` is the real brain |
| **Testing** | Wasn't sure how tests worked | Uses Python's built-in `unittest` with extensive mocking |
| **Export Feature** | Thought there might be something similar | **No export exists** — would need to build from scratch following existing patterns |
| **Status Values** | Assumed only 4 statuses | Need to **add `ABANDONED`** for the new business rule |

## Most Valuable Insights from Each Prompt

1. **Project Structure Prompt:** The discovery that there are **zero external dependencies** was the biggest surprise. This tells me the project was designed for simplicity and portability.

2. **Feature Location Prompt:** Since there was **no existing export functionality**, I learned to infer patterns from `format_task()` (string formatting) and `storage.save()` (file operations). The AI helped me see that CSV export belongs in the **business logic layer**, not the storage layer.

3. **Domain Model Prompt:** The `is_overdue()` method already captured the "overdue" concept. I realized the new "abandoned after 7 days" rule is just an **extension** of existing logic — not a completely new idea.

## Approach to Implementing the New Business Rule

**Rule:** *Tasks overdue >7 days → marked as abandoned, unless HIGH priority.*

**Step-by-step plan:**
1. **Add `ABANDONED` to `TaskStatus`** in `models.py`
2. **Add `mark_overdue_as_abandoned()`** to `task_manager.py` that:
   - Gets all tasks
   - Checks: `due_date < (now - 7 days)` AND `status != DONE` AND `priority != HIGH`
   - Sets `status = ABANDONED` and updates `updated_at`
   - Calls `storage.save()`
3. **Add CLI command** `abandon-old` in `cli.py`
4. **Add unit tests** covering:
   - Task overdue 8 days + LOW priority → should be abandoned
   - Task overdue 8 days + HIGH priority → should NOT be abandoned
   - Task overdue 5 days → should NOT be abandoned (not >7)
   - Task already DONE → should NOT be abandoned

## Strategies for Approaching Unfamiliar Code in the Future

1. **Start with the "front door"** — find the entry point (CLI, main function, or README)
2. **Draw the layers** — separate presentation, logic, storage, and models
3. **Run it before reading it** — seeing the app work makes the code make sense
4. **Read tests as documentation** — tests show exactly what the code is supposed to do
5. **Use AI to confirm, not replace** — form your own hypothesis first, then ask "Am I right?"
6. **Follow the data** — trace where user input goes from start to finish
7. **Check for config files** — `requirements.txt`, `package.json`, etc. reveal the tech stack instantly
