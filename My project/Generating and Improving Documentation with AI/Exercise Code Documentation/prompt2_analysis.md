# Prompt 2: Intent and Logic Explanation

**Prompt I used:**

> I need help documenting the intent and logic behind this code. Please:
>
> ```python
> [paste code here]
> ```
>
> 1. Explain what this code is trying to accomplish at a high level
> 2. Break down the logic step-by-step
> 3. Identify any assumptions or edge cases in the implementation
> 4. Suggest inline comments for complex parts
> 5. Note any potential improvements while maintaining the original functionality

---

## 1. High-Level Intent (The Big Picture)

This code is basically a **"smart to-do list sorter."** Imagine you have a bunch of homework assignments. Some are due tomorrow, some are due next week, some you already finished, and some are marked "URGENT!" This code looks at ALL of them and decides which one you should do first.

It does this by giving each assignment a **"score"** (like points in a video game). The more points, the higher up the list it goes. Then it can show you just the top 5 most important things so you don't get overwhelmed.

---

## 2. Step-by-Step Logic Breakdown

### `calculate_task_score` (The Scoring Machine)

| Step | What it does | Example |
|------|-----------|---------|
| 1 | Give points based on priority level | LOW = 10, MEDIUM = 20, HIGH = 40, URGENT = 60 |
| 2 | Check the due date and add bonus points | Already late? +35. Due today? +20. Due in 2 days? +15. Due in 7 days? +10 |
| 3 | Check if already done and subtract points | DONE? -50. In review? -15 |
| 4 | Check for special tags and add points | "blocker", "critical", or "urgent" tag? +8 |
| 5 | Check how recently it was updated | Updated in last 24 hours? +5 |
| 6 | Add everything up and return the total | Final score! |

### `sort_tasks_by_importance` (The Line-Up Maker)

| Step | What it does |
|------|-----------|
| 1 | For every task, ask `calculate_task_score` for its number |
| 2 | Pair each task with its score (like a name tag) |
| 3 | Sort all the pairs by score, highest first |
| 4 | Peel off the scores, keep only the tasks in order |
| 5 | Return the ordered list |

### `get_top_priority_tasks` (The Top Picks)

| Step | What it does |
|------|-----------|
| 1 | Call `sort_tasks_by_importance` to get the full ordered list |
| 2 | Slice off the first N tasks (like cutting the top of a cake) |
| 3 | Return just those N tasks |

---

## 3. Assumptions & Edge Cases

### Assumptions (Things the code BELIEVES are true)

| Assumption | Risk if wrong |
|-----------|-------------|
| Every task has: `priority`, `due_date`, `status`, `tags`, `updated_at` | If any are missing, the code crashes |
| `datetime.now()` is the correct "right now" time | If the computer clock is wrong, scoring is wrong |
| `TaskPriority` and `TaskStatus` are enums with expected values | If they change, the `priority_weights` dict might break |
| `task.tags` is always a list | If it's `None`, the code **CRASHES**  |
| `task.updated_at` is always a datetime | If it's `None`, the code **CRASHES**  |

### Edge Cases (Weird situations that might break or surprise you)

| Edge Case | What happens | Is it okay? |
|-----------|-------------|-------------|
| `task.due_date` is `None` | Code skips the due date section |  OK |
| `task.tags` is `None` | Code **CRASHES** on `any(...)` |  BUG! |
| `task.updated_at` is `None` | Code **CRASHES** on subtraction |  BUG! |
| Empty task list | `sort_tasks_by_importance` returns `[]` |  OK |
| `limit=0` | `get_top_priority_tasks` returns `[]` |  OK |
| `limit=5` but only 2 tasks | Returns 2 tasks |  OK |
| Two tasks with the SAME score | Python keeps them in original order (stable sort) |  OK, just good to know |
| A DONE task that is also URGENT and overdue | Score = 60 + 35 - 50 = **45** (still positive!) |  Should a done task be "top priority"? |
| Same timestamp, different data | Local wins silently (no update flagged) |  Might hide conflicts |

---

## 4. Suggested Inline Comments (For the tricky parts)

Here's how I would comment the code to make it clearer for someone reading it for the first time:

```python
def calculate_task_score(task):
    """Calculate a priority score for a task based on multiple factors."""
    # Map each priority level to a weight (LOW=1, MEDIUM=2, HIGH=4, URGENT=6)
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Start with base score: priority weight × 10
    # e.g., URGENT = 6 × 10 = 60 points
    score = priority_weights.get(task.priority, 0) * 10

    # --- DUE DATE BONUS ---
    # The closer the deadline, the more urgent it is
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:       # Already late! Big bonus
            score += 35
        elif days_until_due == 0:    # Due today!
            score += 20
        elif days_until_due <= 2:    # Due in next 2 days
            score += 15
        elif days_until_due <= 7:    # Due this week
            score += 10

    # --- STATUS PENALTY ---
    # Done tasks should sink to the bottom of the list
    if task.status == TaskStatus.DONE:
        score -= 50                  # Big penalty for finished work
    elif task.status == TaskStatus.REVIEW:
        score -= 15                  # Smaller penalty (almost done)

    # --- TAG BOOST ---
    # Special keywords mean this task is extra important
    # NOTE: This will crash if task.tags is None! Needs a guard.
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # --- RECENCY BOOST ---
    # Tasks updated recently might need finishing
    # NOTE: This will crash if task.updated_at is None! Needs a guard.
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:        # Updated in the last 24 hours
        score += 5

    return score


def sort_tasks_by_importance(tasks):
    """Sort tasks by calculated importance score (highest first)."""
    # Create (score, task) pairs for every task
    task_scores = [(calculate_task_score(task), task) for task in tasks]

    # Sort by the score (index 0 of each pair), highest to lowest
    # key=lambda x: x[0] tells sorted() to compare only the scores
    # reverse=True puts highest scores first
    sorted_tasks = [task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)]
    return sorted_tasks


def get_top_priority_tasks(tasks, limit=5):
    """Return the top N priority tasks."""
    # Sort everything first, then grab just the first N
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
```

---

## 5. Potential Improvements (keeping the original functionality)

### Improvement 1: Fix the `None` crashes

**What I found:** If `task.tags` or `task.updated_at` is `None`, the code crashes with a `TypeError`. I actually tested this and it broke. This is a real bug in the starter code.

**How to fix it:**
- For tags: `if task.tags and any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):`
- For updated_at: `if task.updated_at:` before calculating `days_since_update`

**Why it matters:** Real data is messy. Sometimes fields are missing. The code should handle that gracefully instead of crashing.

---

### Improvement 2: Name the magic numbers

**What I found:** The numbers `35, 20, 15, 10, 50, 15, 8, 5` are just sitting in the code with no explanation. If someone wants to tweak the scoring (like "overdue should be 50 points, not 35"), they have to hunt through the code to find them.

**How to fix it:** Put them at the top of the file as constants:
```python
OVERDUE_BONUS = 35
DUE_TODAY_BONUS = 20
DONE_PENALTY = 50
TAG_BOOST = 8
# etc.
```

**Why it matters:** Makes the code way easier to maintain. You can see all the scoring rules in one place.

---

### Improvement 3: Add type hints

**What I found:** The functions don't have type hints, so my IDE (VS Code) couldn't help me with autocomplete or catch mistakes. I kept having to check what types things were.

**How to fix it:** Add hints like:
```python
def calculate_task_score(task: Task) -> int:
def sort_tasks_by_importance(tasks: list[Task]) -> list[Task]:
```

**Why it matters:** Helps prevent bugs and makes the code self-documenting. Your IDE can warn you if you pass the wrong type.

---

### Improvement 4: Validate the `limit` parameter

**What I found:** `get_top_priority_tasks` doesn't check if `limit` is negative. If someone passes `-1`, Python slicing works weirdly and returns almost the whole list except the last item. That's confusing!

**How to fix it:** Add:
```python
if limit < 0:
    raise ValueError("limit must be 0 or positive")
```

**Why it matters:** Fail fast with a clear error instead of weird, unexpected behavior.

---

### Improvement 5: Consider caching scores

**What I found:** Every time you sort, you recalculate ALL scores. For a small list this is fine, but for 1000+ tasks it might be slow.

**How to fix it:** Store the score on the task object after calculating once. But you'd need to recalculate if the task changes, so it's tricky.

**Why it matters:** Could speed things up in a real app with lots of tasks. Not urgent for the starter code, but worth thinking about.

---

### Improvement 6: Make the default limit configurable

**What I found:** The default `limit=5` is hardcoded. What if the user wants to see 10 tasks by default? You'd have to edit the code.

**How to fix it:** Read from a config file or environment variable, or pass it as a parameter from the CLI.

**Why it matters:** One less place to edit code when user preferences change.

---

### Improvement 7: Add a "force zero score for DONE tasks" rule

**What I found:** A DONE task can still score positive if it's URGENT and overdue:
```
Score = 60 (urgent) + 35 (overdue) - 50 (done) = 45
```
It still scores positive! Should a finished task really show up in "top priority"?

**How to fix it:** Add:
```python
if task.status == TaskStatus.DONE:
    return 0  # or some very negative number
```
Or make the DONE penalty bigger than any possible positive score.

**Why it matters:** Finished tasks shouldn't clutter the "top priority" list. If it's done, it's done!
