# Code Understanding Journal

For the Python Task Manager

## How I Used AI

I used AI to help me understand this code because honestly, jumping between 4 different files was confusing. I would look at one file, guess what it did, then ask the AI if I was right. A lot of times I was wrong, and the AI corrected me. This journal is what I figured out after going back and forth a few times.

---

## Part 1: Task Creation & Status Updates

### Files Involved

| File | What It Does |
|------|--------------|
| `cli.py` | Reads what you type in the terminal and figures out which command to run |
| `task_manager.py` | The main brain. It takes your command and actually does the work |
| `models.py` | Defines what a Task is — basically a blueprint with title, priority, status, dates, tags |
| `storage.py` | Saves everything to a JSON file so you don't lose your tasks when you close the program |

### What I Learned

**Creating a task:**

When you run `python cli.py create "Buy milk"`, here's what happens:

1. `cli.py` reads your command and calls `task_manager.create_task()`
2. The manager takes your info and builds a `Task` object using the blueprint in `models.py`
3. I didn't get why we needed a whole class for this at first, but it's because a task has a bunch of stuff attached to it — status, dates, tags — and the class keeps it all organized
4. The manager gives the new task to `storage.py`, which saves it in a dictionary and writes it to `tasks.json`

**Updating status to DONE:**

1. You type `python cli.py status <id> done`
2. The manager asks storage to find that task by its ID
3. If it finds it, it calls `task.mark_as_done()` — this flips the status to DONE and records the exact time
4. Storage saves everything back to the JSON file

### Design Patterns

I think this is something like MVC (Model-View-Controller). `models.py` is the Model, `cli.py` is like the View/Controller, `task_manager.py` is the brain, and `storage.py` is the database part. I'm not 100% sure if it's "real" MVC but that's what it reminds me of.

Also, `TaskStorage` hides all the saving details from the rest of the app. The manager just says "save" and doesn't care if it's JSON or a real database or whatever.

---

## Part 2: Task Prioritization System

### What I Thought at First

I thought priority was just a number stored in the task, like `priority = 3`, and maybe the list command sorted by it. I didn't think it was anything special.

### What I Actually Found

In `models.py` there's this thing called an `Enum`:

```python
class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
```

I didn't know what an Enum was. I had to ask the AI. Turns out it's basically a dropdown menu — you can ONLY pick 1, 2, 3, or 4. You can't invent a "5" or type "super urgent" because the code will throw an error.

Also in `cli.py`:

```python
create_parser.add_argument("-p", "--priority", help="Task priority (1-4)",
                           type=int, choices=[1, 2, 3, 4], default=2)
```

The CLI literally only accepts 1, 2, 3, or 4. No other numbers.

And when you filter by priority, `storage.py` just loops through all tasks and checks if `task.priority == priority`.

### Questions I Had

**Q: What happens if you try priority 5?**
A: The CLI blocks it. But if you somehow bypass the CLI and call `TaskManager` directly with 5, Python throws a `ValueError` because `TaskPriority(5)` doesn't exist.

**Q: How does the app know "URGENT" means 4?**
A: The Enum maps the name to the number. When saving to JSON, it saves the number (4). When loading back, it recreates `TaskPriority(4)` which knows its name is `URGENT`.

**Q: Can you change priority after creating the task?**
A: Yes, there's an `update_task_priority` method.

### Key Insights

- The CLI checks your input, and the Enum checks the data model. It's like double validation.
- The computer saves numbers, but humans see words like "HIGH" or "URGENT". I didn't realize that's a common pattern but it makes sense.

---

## Part 3: Data Flow When Marking a Task Complete

### What Happens Step by Step

When you mark a task as done, here's the order:

1. You type `python cli.py status <task_id> done` in the terminal
2. `cli.py` parses your command and calls `task_manager.update_task_status(task_id, "done")`
3. The manager turns the string `"done"` into `TaskStatus.DONE`
4. Since the new status is DONE, the manager asks `storage.py` to find the task by its ID
5. If found, the manager calls `task.mark_as_done()` on that task object
6. `mark_as_done()` does 3 things:
   - Sets `status` to `DONE`
   - Sets `completed_at` to the current time
   - Updates `updated_at` to the current time
7. The manager tells storage to save everything
8. `storage.py` opens `tasks.json`, converts all the Task objects to JSON text, and writes it to disk

### What Changes in the Task

| Thing | Before | After |
|-------|--------|-------|
| status | `TODO`, `IN_PROGRESS`, or `REVIEW` | `DONE` |
| completed_at | `None` | the exact time you finished |
| updated_at | old time | current time |

### Things That Could Go Wrong

1. **Wrong ID:** If you type a bad task ID, storage can't find it and returns `None`. The manager returns `False` and nothing happens.
2. **Disk fails:** If your computer is out of space or the file is locked, `storage.save()` prints an error. But the task in memory was already marked done, so if you restart the program it might look undone again. That seems like a bug.
3. **Two people at once:** If two people run the CLI at the same time, they might both read the file, then one overwrites the other. This app isn't built for multiple users.

### How It Saves

`storage.py` has a `TaskEncoder` that translates Python objects into JSON. It saves the priority as a number and the status as a string. It also converts all the datetime objects into text format so JSON can handle them.

When loading back, `TaskDecoder` does the reverse — it sees `"status": "done"` and turns it back into `TaskStatus.DONE`.

---

## Part 4: Reflection

### Architecture Overview

The app has 4 layers:

1. **CLI (`cli.py`)** — where you type commands
2. **TaskManager (`task_manager.py`)** — the brain that decides what to do
3. **TaskStorage (`storage.py`)** — saves and loads data from a file
4. **Models (`models.py`)** — defines what a task looks like

### The Three Features

- **Task Creation:** You type a command, the CLI sends it to the manager, the manager builds a Task object and tells storage to save it.
- **Prioritization:** Tasks get a priority number 1-4. The Enum makes sure only valid numbers are used. You can filter the list to show only certain priorities.
- **Completion:** You send a "done" command. The manager finds the task, runs `mark_as_done()`, and saves the file.

### One Interesting Thing I Found

The `Enum` thing was actually pretty cool. I didn't know Python had this built-in. It's basically a dropdown menu that stops you from typing stupid stuff. I can see why that's useful — if someone accidentally types `"dno"` instead of `"done"`, the Enum catches it immediately instead of letting bad data spread everywhere.

### What Confused Me the Most

At first, I didn't understand why `mark_as_done()` needed to be its own special method when there was already a generic `update()` method. I thought it was just extra code. But after tracing the flow, I realized that marking something done is special because it updates TWO things at once — the status AND the completion time. If you just used `update()`, you might forget to record the finish time. Having a dedicated method means you can't forget. It's like a safety guard.

### How the AI Helped

The most helpful thing was when I stopped asking "what does this file do?" and started asking "what happens when I type this command?" That made me look at how the files talk to each other instead of reading them one by one. I still don't understand everything perfectly, but I can trace a command from start to finish now.
