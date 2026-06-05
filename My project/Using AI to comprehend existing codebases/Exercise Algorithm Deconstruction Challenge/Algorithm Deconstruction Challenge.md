# Exercise Algorithm Deconstruction Challenge
## Python 
---

## Contents

- [1. Algorithm Selection](#1-algorithm-selection)
- [2. AI Prompts Used](#2-ai-prompts-used)
- [3. Simple Explanation](#3-simple-explanation)
- [4. Visual Diagram](#4-visual-diagram)
- [5. Technical Deep Dive](#5-technical-deep-dive)
- [6. Insights & Learning Points](#6-insights--learning-points)
- [7. Reflection Questions](#7-reflection-questions)
- [8. Improvement Proposals](#8-improvement-proposals)
- [9. Original Code](#9-original-code)
- [10. Summary](#10-summary)

---

## 1. Algorithm Selection

I chose **Algorithm 1: Task Priority Sorting** because it was the most intuitive when I first read through the three options. The text parser (Algorithm 2) had a lot of regex that I am still learning, and the two-way sync (Algorithm 3) felt overwhelming with all the conflict resolution logic.

The sorting algorithm is basically just math — adding and subtracting numbers to figure out what is most important. It also connects to the actual Task Manager CLI in this repo (`use-cases/code-algorithms/python/TaskManager`), so it felt like real code, not just a classroom example.

---

## 2. AI Prompts Used

I used an AI assistant to help me break down the algorithm. Here are the prompts I tried and what I learned:

| # | Prompt | What I Learned |
|---|--------|----------------|
| 1 | Explain this algorithm like I am 5. What is it trying to do? | It is a robot that gives every task an urgency number and sorts by it. Simple, but accurate. |
| 2 | Draw a flow diagram showing how data moves through each function. | There are 3 functions working as a pipeline: calculate score -> sort -> pick top N. |
| 3 | What are the magic numbers and what do they represent? | 35, 20, 15, 10 are not random — they are tiers for how urgent the due date is. |
| 4 | What are the edge cases and hidden bugs? | A DONE task can still score high if it is also overdue and tagged critical. Weird. |
| 5 | How would you explain this to a junior developer in one minute? | The video game power level analogy in Section 3. |
| 6 | What patterns from this code can I use in other projects? | `.get()` with defaults, `any()` with generators, and the Decorate-Sort-Undecorate pattern. |

---

## 3. Simple Explanation

Imagine you have chores on sticky notes on your fridge:

- Clean your room (not urgent)
- Feed the dog (due tonight!)
- Buy mom a birthday gift (due tomorrow!)
- Take out the trash (already done)

You need to know which one to do first.

This algorithm is like a **robot helper** that gives every chore an **urgency number**. Higher number = do this first.

### How the robot scores each chore:

**1. How important is it?**
- LOW = 10 points
- MEDIUM = 20 points
- HIGH = 40 points
- URGENT = 60 points

**2. When is it due?**
- Already late = +35 points
- Due today = +20 points
- Due in 1-2 days = +15 points
- Due this week = +10 points

**3. Is it already done?**
- DONE = -50 points (sinks to bottom)
- In review = -15 points

**4. Does it have scary words?**
If it says "blocker" or "critical" or "urgent" = +8 points

**5. Was it just updated?**
- Updated in the last day = +5 points

Then the robot sorts everything from highest to lowest score. The top ones are what you do first!

---

## 4. Visual Diagram

### The Big Picture Flow

```
START: Unsorted Tasks
    |
    v
+----------------------------+
| calculate_task_score()     |
|   (runs for EACH task)     |
|                            |
|  1. Base Score             |
|     Priority x 10          |
|     LOW=10, MEDIUM=20,     |
|     HIGH=40, URGENT=60     |
|                            |
|  2. Due Date Bonus         |
|     Overdue    +35         |
|     Today      +20         |
|     <= 2 days  +15         |
|     <= 7 days  +10         |
|                            |
|  3. Status Penalty         |
|     DONE   -50             |
|     REVIEW -15             |
|                            |
|  4. Tag Boost              |
|     blocker/critical/      |
|     urgent +8              |
|                            |
|  5. Recency Boost          |
|     Updated < 1 day +5     |
|                            |
|     => FINAL SCORE         |
+----------------------------+
    |
    v
+----------------------------+
| sort_tasks_by_importance() |
|   Sort by score (high->low)|
+----------------------------+
    |
    v
+----------------------------+
| get_top_priority_tasks()   |
|   Take first N (default 5) |
+----------------------------+
```

### Scoring Cheat Sheet

| Factor | Points | Why? |
|--------|--------|------|
| Priority Base | x10 | Foundation of urgency |
| Overdue | +35 | Late tasks are emergencies |
| Due Today | +20 | Very urgent |
| Due <=2 Days | +15 | Pretty urgent |
| Due <=7 Days | +10 | Somewhat urgent |
| Status = DONE | -50 | Completed = not important |
| Status = REVIEW | -15 | Almost done, lower priority |
| Critical Tags | +8 | Business-critical marker |
| Recent Update | +5 | Freshly touched = active |

### Example Scoreboard (calculated by hand)

| Task | Priority | Due Date | Status | Tags | Updated | **Score** | Rank |
|------|----------|----------|--------|------|---------|-----------|------|
| Fix login bug | URGENT | Yesterday | TODO | blocker | 2 hrs ago | 60+35+8+5 = **108** | #1 |
| Write API tests | HIGH | Today | TODO | - | 1 day ago | 40+20 = **60** | #2 |
| Review PR #42 | MEDIUM | Tomorrow | REVIEW | - | 3 days ago | 20+15-15 = **20** | #3 |
| Update README | LOW | Next week | DONE | - | 5 days ago | 10+10-50 = **-30** | #4 |

---

## 5. Technical Deep Dive

This is what I understand about the code, line by line. I am still learning, so some of this might be basic, but it is what clicked for me.

### 5.1 calculate_task_score()

This function does not change anything outside itself — it just takes a task, does math, and returns a number. The AI told me this is called a **pure function**, which makes it easier to test.

**Dictionary Lookup with Default**
```python
score = priority_weights.get(task.priority, 0) * 10
```
I used to write code that crashed if a key was missing from a dictionary. `.get(key, 0)` is way safer — if the priority is weird or unknown, it just returns 0. I am going to use `.get()` more in my own code.

**Date Bucket Logic**
```python
if days_until_due < 0:      # Overdue
    score += 35
elif days_until_due == 0:   # Today
    score += 20
elif days_until_due <= 2:   # Next 2 days
    score += 15
elif days_until_due <= 7:   # This week
    score += 10
```
At first I wondered why they did not use a smooth formula like `30 / days_until_due`. Then I realized: what if it is due today (0 days)? You would divide by zero! Also, buckets match how people actually think — "this week" vs "next week" is clearer than some decimal. Smart choice.

**any() with Generator Expression**
```python
if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
    score += 8
```
I had seen `any()` before but never used it. It stops checking as soon as it finds ONE match — it does not waste time on the rest. The `for tag in task.tags` part is a **generator expression**, so it does not build a whole list in memory. I need to practice this.

### 5.2 sort_tasks_by_importance()

```python
def sort_tasks_by_importance(tasks):
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks
```

This took me a while. The AI explained it is called a **Schartzian Transform** (or Decorate-Sort-Undecorate):

1. **Decorate:** Stick the score on each task like a sticky note: `(score, task)`
2. **Sort:** Python sorts tuples by the first number automatically
3. **Undecorate:** Peel off the sticky note, keep just the task: `[task for _, task in ...]`

The `_` means we do not care about the score anymore. Neat Python trick.

The reason they do this instead of calling `calculate_task_score` inside the sort comparison is **efficiency**. With 100 tasks, calculating once per task is way faster than recalculating during every comparison.

### 5.3 get_top_priority_tasks()

```python
def get_top_priority_tasks(tasks, limit=5):
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
```

Super simple — just list slicing `[:limit]`. Default is 5, which is a nice daily to-do number. If you have fewer than 5 tasks, Python just returns what you have. No crashes.

---

## 6. Insights & Learning Points

These are the things that stuck with me after studying this algorithm:

| # | What I Learned | Why It Matters |
|---|----------------|---------------|
| 1 | **Scores are calculated on the fly** | The score is not saved anywhere. Every time you sort, it recalculates. If a task becomes overdue at midnight, its score jumps up automatically. No database updates needed. |
| 2 | **Negative penalties are stronger than bonuses** | The -50 for DONE is almost as big as the URGENT base (60). This is on purpose — it guarantees completed tasks sink to the bottom, even if they are overdue and tagged critical. |
| 3 | **Date buckets are better than fancy math** | Discrete buckets (overdue/today/2days/7days) instead of a continuous formula makes the code readable and avoids division-by-zero edge cases. |
| 4 | **Time is a decision factor in other algorithms too** | Algorithm 3 (Task List Merging) uses timestamps to resolve conflicts. Algorithm 1 uses dates to weight urgency. Time-based logic is huge in real software. |
| 5 | **Python's any() is a superpower** | The tag-checking line is both readable and memory-efficient. It streams through tags until it finds a match. I want to use this more. |
| 6 | **The Schartzian Transform is a real thing** | I thought the tuple-sorting trick was random, but it is a named pattern from Perl. It works great in Python too. |
| 7 | **Magic numbers should be configurable** | 35, 20, 15, 10, 50, 15, 8, 5 are hardcoded. A product manager might want to tweak them. Moving them to a config file would improve maintainability. |
| 8 | **Three small functions beat one giant function** | The algorithm is split into calculate -> sort -> limit. Each does one thing. This makes it easier to test and understand. I have a bad habit of writing giant functions, so this was a good reminder. |

---

## 7. Reflection Questions

### Q1: How did the AI's explanation change your understanding?

Before the AI, I looked at `score += 35` and honestly thought it was just some random number. The code looked like a pile of math that somehow produced a sorted list, but I did not understand why those specific numbers were chosen.

After the AI explained it, I realized **35 is not random** — it is a deliberate overdue penalty tier that makes overdue tasks jump ahead of almost everything except URGENT tasks due today. The AI helped me see the scoring formula as a **weighted decision system**, like credit scores or search engine rankings.

The AI also taught me about the **Schartzian Transform** — I had no idea that attaching data to objects before sorting was a named pattern. I just thought it was a weird Python trick. Now I see this algorithm as a **business rules engine** rather than just math. That shift was huge for me.

### Q2: What aspects were still difficult to understand?

The thing that still bugs me is **how the different factors interact**. For example, what happens if a task is:

- Priority: URGENT (+60 base)
- Due: Yesterday (+35 overdue)
- Status: DONE (-50 penalty)
- Tags: "blocker" (+8)
- Updated: 2 hours ago (+5)

**Final score: 60 + 35 - 50 + 8 + 5 = 58**

This DONE task still scores 58 — higher than a MEDIUM task due tomorrow (20 + 15 = 35). Should a DONE task EVER show up in a top priority list? The algorithm does not really answer this. The AI helped me spot the issue, but I think the right behavior depends on what the business actually wants, not just what the code does.

Another thing that confused me: the JavaScript implementation uses different weights than Python. In Python, URGENT is weight 6 (so 60 points), but in JavaScript it is weight 4 (so 40 points). The exercise shows three languages with different numbers but does not explain why. I am not sure if that is a mistake or intentional.

### Q3: How would you explain this to another junior developer?

I would say: "Imagine every task is a player in a video game, and they all have a power level. The power level starts based on how important the task is — URGENT tasks start at 60, LOW tasks start at 10. Then we add bonus points: +35 if it is already late, +20 if due today, +15 if due soon. We subtract points if it is done (-50) or in review (-15). If it has scary tags like blocker, we add +8. Finally, we sort everyone by power level and pick the top 5. Highest power level = do this first."

Then I would show them the code and say: "See these three functions? One calculates the power level, one sorts by it, and one picks the top N. Each function does exactly one thing. That is how we keep code clean."

I think the video game analogy works because most people understand power levels and rankings naturally. It is less intimidating than talking about weighted scoring algorithms.

### Q4: Did you test this understanding against AI?

Yes — basically this whole document is me testing my understanding. I asked the AI to:

1. Explain the algorithm like I am 5
2. Draw flow diagrams
3. Identify magic numbers and their meanings
4. Find edge cases and bugs
5. Suggest improvements

The AI confirmed that I understood the scoring tiers correctly, but it also revealed the **DONE + OVERDUE edge case** that I had not thought about. I then asked the AI to compare the Python, JavaScript, and Java implementations, and it pointed out the **weight inconsistencies** between languages (Python URGENT = 6, JS/Java URGENT = 4).

Cross-checking my own understanding against the AI helped me feel confident that I got the core logic right, while also showing me where the exercise materials themselves might have issues. It was like having a study partner who knows way more than me but does not judge me for asking basic questions.

### Q5: How might you improve the algorithm?

These are the improvements I would suggest if I were working on this project:

**1. Filter out DONE tasks completely**
Instead of penalizing DONE tasks with -50, I would remove them before sorting. A completed task should never appear in a "what should I do next?" list.

```python
active_tasks = [t for t in tasks if t.status != TaskStatus.DONE]
sorted_tasks = sort_tasks_by_importance(active_tasks)
```

**2. Make weights configurable**
Move the hardcoded numbers to a config dictionary so product managers can tweak them without a developer changing the code.

```python
SCORING_CONFIG = {
    "priority_weights": {"LOW": 1, "MEDIUM": 2, "HIGH": 4, "URGENT": 6},
    "due_date_boosts": {"overdue": 35, "today": 20, "soon": 15, "this_week": 10},
    "status_penalties": {"DONE": 50, "REVIEW": 15},
    "tag_boost": 8,
    "recency_boost": 5
}
```

**3. Add user-defined importance**
Let users manually star or pin tasks for an extra boost (like +25). This handles edge cases the math cannot predict.

**4. Normalize scores to 0-100**
The max possible score is 108. A 0-100 scale would be easier to show in a UI with progress bars or color badges. Users understand percentages better than raw numbers.

**5. Cache the current time**
If sorting 10,000 tasks, calling `datetime.now()` for every single task is wasteful. Cache it at the start of the function.

```python
def sort_tasks_by_importance(tasks):
    now = datetime.now()  # Calculate once!
    task_scores = [(calculate_task_score(task, now), task) for task in tasks]
    ...
```

**6. Fix language inconsistencies**
The Python, JavaScript, and Java versions should use the same weights. Right now they do not match, which is confusing for anyone trying to understand the algorithm across languages.

---

## 8. Improvement Proposals

| Aspect | Current | My Proposed Version |
|--------|---------|---------------------|
| DONE tasks | Penalized (-50) but still sorted | Filtered out entirely |
| Magic numbers | Hardcoded in functions | Configurable dictionary |
| User control | None | Manual star/pin boost |
| Score display | Raw number (e.g., 108) | Normalized 0-100 scale |
| Performance | Recalculates now() per task | Caches now() once per sort |
| Cross-language | Inconsistent weights | Standardized weight table |

### My Improved Pseudocode

```python
# Configuration (editable without touching logic)
SCORING_RULES = {
    "priority": {"LOW": 10, "MEDIUM": 20, "HIGH": 40, "URGENT": 60},
    "due_date": {"overdue": 35, "today": 20, "within_2_days": 15, "within_week": 10},
    "status_filter": ["DONE"],  # Exclude these entirely
    "status_penalty": {"REVIEW": 15},
    "critical_tags": ["blocker", "critical", "urgent"],
    "tag_boost": 8,
    "recency_hours": 24,
    "recency_boost": 5,
    "user_pin_boost": 25
}

def calculate_task_score_v2(task, config, current_time):
    """Improved version with config injection and time caching."""
    if task.status in config["status_filter"]:
        return None  # Signal to exclude

    score = config["priority"].get(task.priority, 0)

    # Due date logic with cached time
    if task.due_date:
        days_until = (task.due_date - current_time).days
        if days_until < 0:
            score += config["due_date"]["overdue"]
        elif days_until == 0:
            score += config["due_date"]["today"]
        elif days_until <= 2:
            score += config["due_date"]["within_2_days"]
        elif days_until <= 7:
            score += config["due_date"]["within_week"]

    # Status penalties (only for non-filtered statuses)
    if task.status in config["status_penalty"]:
        score -= config["status_penalty"][task.status]

    # Tag boost
    if any(tag in config["critical_tags"] for tag in task.tags):
        score += config["tag_boost"]

    # Recency boost
    hours_since_update = (current_time - task.updated_at).total_seconds() / 3600
    if hours_since_update < config["recency_hours"]:
        score += config["recency_boost"]

    # User pin boost
    if getattr(task, "is_pinned", False):
        score += config["user_pin_boost"]

    return score

def sort_tasks_by_importance_v2(tasks, config=None):
    """Improved sorting with filtering and normalization."""
    config = config or SCORING_RULES
    now = datetime.now()

    # Calculate scores and filter out excluded tasks
    scored_tasks = []
    for task in tasks:
        score = calculate_task_score_v2(task, config, now)
        if score is not None:
            scored_tasks.append((score, task))

    # Sort by score descending
    scored_tasks.sort(key=lambda x: x[0], reverse=True)

    # Optional: Normalize to 0-100
    if scored_tasks:
        max_score = scored_tasks[0][0]
        normalized = [(min(100, int((s/max_score)*100)), t) for s, t in scored_tasks]
        return [task for _, task in normalized]

    return [task for _, task in scored_tasks]
```

---

## 9. Original Code

Here is the original Python code from the exercise, for reference while reading my analysis:

```python
def calculate_task_score(task):
    """Calculate a priority score for a task based on multiple factors."""
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }
    score = priority_weights.get(task.priority, 0) * 10

    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:
            score += 35
        elif days_until_due == 0:
            score += 20
        elif days_until_due <= 2:
            score += 15
        elif days_until_due <= 7:
            score += 10

    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score

def sort_tasks_by_importance(tasks):
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks

def get_top_priority_tasks(tasks, limit=5):
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
```

---

## 10. Summary

This exercise helped me realize that algorithms are not just math — they are **business rules written as code**. Every number in the scoring formula represents a decision someone made about what is important.

Before this exercise, I would have looked at this code and just thought "oh, it sorts tasks." Now I can see the **weighted decision system** underneath, the **efficiency patterns** (Schartzian Transform, generator expressions), and the **design trade-offs** (date buckets vs. linear formulas).

The biggest thing I learned is that understanding the **why** behind each number is just as important as understanding the **how**. The -50 for DONE is not just a penalty — it is a business rule saying "completed tasks should never be top priority." The +35 for overdue is not just a bonus — it is a rule saying "late tasks are emergencies."

I also learned that I need to be careful about **magic numbers** in my own code. If I had written this from scratch, I probably would have hardcoded everything too. But now I see how much better it is to make those numbers configurable.

Finally, I am walking away with concrete patterns I want to use in my own projects:
- `.get()` with defaults for safe dictionary lookups
- `any()` with generator expressions for efficient searching
- The Decorate-Sort-Undecorate pattern for sorting by computed values
- Breaking big problems into small, single-purpose functions

This was a really useful exercise. I feel like I actually understand this algorithm now — not just on the surface, but deep enough to explain it to someone else and even suggest improvements.
