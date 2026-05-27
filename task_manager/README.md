# Task Manager CLI

A simple command-line task manager I built (and extended) for my codebase exploration exercise.

## What It Does

This is a Python terminal app that lets you:
- Create tasks with titles, descriptions, priorities, due dates, and tags
- List, update, and delete tasks
- Mark tasks as done (or abandoned)
- Export all tasks to a CSV file
- Run a "cleanup" command that auto-marks very old overdue low-priority tasks as abandoned

## How to Run It

Make sure you are standing in the **outer** `task_manager` folder (the one that contains the inner `task_manager` folder):

```bash
cd C:\Users\Moses\Downloads\task_manager
```

Then run any of these commands:

### Create a task
```bash
python -m task_manager.cli create "Buy groceries" -d "Milk and eggs" -p 2 -u 2026-06-01 -t "personal,shopping"
```

### List all tasks
```bash
python -m task_manager.cli list
```

### Mark a task as done
```bash
python -m task_manager.cli status <task-id> done
```

### Export to CSV
```bash
python -m task_manager.cli export my_tasks.csv
```

### Run cleanup (marks old overdue low-priority tasks as abandoned)
```bash
python -m task_manager.cli cleanup
```

### Show stats
```bash
python -m task_manager.cli stats
```

## Files in This Project

| File | What It Does |
|------|-------------|
| `models.py` | Defines Task, TaskPriority, and TaskStatus. Also has the business rules (like when a task is "overdue" or "abandonable"). |
| `app.py` | The TaskManager class — the "boss" that creates, updates, lists, exports, and cleans up tasks. |
| `storage.py` | Handles reading and writing tasks to `tasks.json`. |
| `cli.py` | The command-line interface. Parses what you type and calls the right methods in `app.py`. |
| `__init__.py` | Empty file that tells Python this folder is a package. |

## Architecture

I think of it like a sandwich:
- **Top layer (CLI)**: You type commands here
- **Middle layer (App)**: The boss decides what to do
- **Bottom layer (Storage + Models)**: Saves data and defines what a task looks like

## New Features I Added

### 1. CSV Export
Added an `export` command that dumps all tasks to a CSV file with columns for id, title, description, priority, status, due date, timestamps, and tags.

### 2. Auto-Abandon Cleanup
Added a `cleanup` command that checks all tasks. If a task is:
- More than 7 days overdue, AND
- Low or medium priority (not high/urgent), AND
- Not already done or abandoned

...then it gets marked as **ABANDONED** automatically.

This was the business rule I had to implement for Part 4 of the exercise.

## Troubleshooting Notes

- If you get `ModuleNotFoundError: No module named 'task_manager'`, make sure you are running the command from the **outer** folder (not inside `task_manager\task_manager`).
- Make sure the `__init__.py` file exists in the inner `task_manager` folder.
- The app stores everything in `tasks.json` in the outer folder.

## What I Learned

- Python packages need `__init__.py` to work as modules
- JSON is used for simple storage (no database needed)
- Business rules belong in `models.py`, not scattered everywhere
- Always test after each small change
