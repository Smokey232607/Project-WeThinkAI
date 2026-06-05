# Prompt 1: Comprehensive Function Documentation

**Prompt I used:**

> Please create comprehensive documentation for this function following Python docstring conventions (Google style):
>
> ```python
> [paste function code here]
> ```
>
> The documentation should include:
> 1. A clear description of what the function does
> 2. All parameters with types and descriptions
> 3. Return value with type and description
> 4. Any exceptions or errors that might be thrown
> 5. Example usage
> 6. Any important notes or edge cases developers should be aware of

---

## Module Overview: `task_priority`

This module figures out which tasks are the most important and puts them in order. It gives each task a "score" (kind of like points in a video game) and then sorts them so the highest-scoring tasks are first.

---

## Function 1: `calculate_task_score(task)`

### What it does

This function looks at one task and calculates a number score. The higher the number, the more important/urgent the task is. It checks the priority level, due date, status, tags, and when it was last updated.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `task` | `Task` | A task object that needs to have these properties: `priority` (TaskPriority), `due_date` (datetime or None), `status` (TaskStatus), `tags` (list), `updated_at` (datetime) |

### Returns

| Type | Description |
|------|-------------|
| `int` | The priority score. This can be **negative** if the task is already done (because done tasks get -50 points). |

### Exceptions

| Exception | When it happens |
|-----------|----------------|
| `AttributeError` | If the task object doesn't have the properties the function expects (like `priority`, `due_date`, etc.) |

### Example Usage

```python
# Make a task that's URGENT and due today
my_task = Task("Fix the login bug")
my_task.priority = TaskPriority.URGENT
my_task.due_date = datetime.now()  # due right now!
my_task.status = TaskStatus.TODO
my_task.tags = ["blocker"]
my_task.updated_at = datetime.now()

score = calculate_task_score(my_task)
print(score)  # Should be pretty high!
```

### Important Notes & Edge Cases

1. **Overdue tasks** get +35 points (very high priority!)
2. **Tasks due TODAY** get +20 points
3. **Tasks due in 2 days** get +15 points
4. **Tasks due in 7 days** get +10 points
5. **DONE tasks** lose 50 points (so they sink to the bottom)
6. **Tasks in REVIEW** lose 15 points
7. **Tags** like "blocker", "critical", "urgent" add +8 points
8. **Tasks updated in the last 24 hours** get +5 points
9. If a task has **NO due_date**, it gets NO extra points for that section
10. The score **can be negative**! A DONE task might score -50 or worse
11. **⚠️ BUG I FOUND:** If `task.tags` is `None` instead of a list, the code **crashes** on the `any(...)` line
12. **⚠️ BUG I FOUND:** If `task.updated_at` is `None`, the code **crashes** on the `days_since_update` line

---

## Function 2: `sort_tasks_by_importance(tasks)`

### What it does

Takes a list of tasks, calculates a score for each one using `calculate_task_score()`, and returns a new list sorted from highest score to lowest score.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `tasks` | `list[Task]` | A list of Task objects. Can be empty. |

### Returns

| Type | Description |
|------|-------------|
| `list[Task]` | A new list of Task objects in order of importance. The original list is **NOT** changed. |

### Exceptions

| Exception | When it happens |
|-----------|----------------|
| `TypeError` | If you pass something that's not a list, or if the list contains things that aren't Task objects |

### Example Usage

```python
my_tasks = [task1, task2, task3]
sorted_tasks = sort_tasks_by_importance(my_tasks)
# sorted_tasks[0] is the most important one!
# my_tasks is still in its original order
```

### Important Notes

- This returns a **NEW list**. The original list stays the same. I had to check this because I wasn't sure if `sorted()` modifies the original or not. (It doesn't — it makes a copy.)
- The sorting is **"stable,"** which means if two tasks have the exact same score, they stay in the same order they were in before. I learned this from the Python docs.
- Every time you call this, it recalculates ALL the scores. If you have a ton of tasks this might be slow, but for the starter code it's fine.

---

## Function 3: `get_top_priority_tasks(tasks, limit=5)`

### What it does

Sorts all the tasks by importance, then returns only the top N. Like getting the leaderboard but only showing the top 5 players.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `tasks` | `list[Task]` | A list of Task objects. |
| `limit` | `int` | How many tasks to return. Default is 5. Must be 0 or higher. |

### Returns

| Type | Description |
|------|-------------|
| `list[Task]` | The top `limit` most important tasks. Might be fewer than `limit` if there aren't enough tasks. |

### Exceptions

| Exception | When it happens |
|-----------|----------------|
| `TypeError` | If `tasks` isn't a list |
| `ValueError` | If `limit` is negative (the original code doesn't check this, but it should!) |

### Example Usage

```python
all_my_tasks = [task1, task2, task3, task4, task5, task6]
top_3 = get_top_priority_tasks(all_my_tasks, limit=3)
# top_3 has only the 3 most important tasks!
```

### Important Notes

- If `limit=0`, returns an empty list.
- If there are only 2 tasks but `limit=5`, returns both tasks.
- The default `limit=5` is a **"magic number"** — in a real app you might want to make this configurable instead of hardcoded.
