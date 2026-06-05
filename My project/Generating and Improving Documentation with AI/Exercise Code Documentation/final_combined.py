# ============================================================
# FINAL COMBINED VERSION
# ============================================================
# This is my polished version that combines:
#   - The documentation from Prompt 1
#   - The improvements and fixes from Prompt 2
#   - My own testing and fixes (the None guards)
#   - Type hints (I learned these in another class)
#   - Named constants for the magic numbers
#
# I tried to keep the original behavior exactly the same,
# just make it safer and clearer to read.
# ============================================================

from datetime import datetime
from typing import List, Optional
from models import TaskStatus, TaskPriority, Task


# --- Configuration: Scoring Weights ---
# These numbers control how important each factor is.
# Change them here to tweak the sorting behavior!
# I moved these from being hidden in the function to the top
# so they're easy to find and adjust.
PRIORITY_WEIGHTS = {
    TaskPriority.LOW: 1,
    TaskPriority.MEDIUM: 2,
    TaskPriority.HIGH: 4,
    TaskPriority.URGENT: 6
}

# Due date bonuses (closer deadline = bigger bonus)
OVERDUE_BONUS = 35
DUE_TODAY_BONUS = 20
DUE_SOON_BONUS = 15       # 1-2 days
DUE_THIS_WEEK_BONUS = 10  # 3-7 days

# Status penalties (completed work should sink to bottom)
DONE_PENALTY = 50
REVIEW_PENALTY = 15

# Tag boost (special keywords make task more important)
IMPORTANT_TAGS = ["blocker", "critical", "urgent"]
TAG_BOOST = 8

# Recency boost (recently touched tasks get a nudge)
RECENCY_BOOST = 5
RECENCY_WINDOW_DAYS = 1


def calculate_task_score(task: Task) -> int:
    """Calculate a priority score for a task based on multiple factors.

    Higher score = more urgent/important. Can be negative for done tasks.

    Args:
        task: A Task object with priority, due_date, status, tags,
              and updated_at properties.

    Returns:
        int: The calculated priority score.

    Raises:
        AttributeError: If the task is missing required attributes.

    Example:
        >>> t = Task("Fix login bug")
        >>> t.priority = TaskPriority.HIGH
        >>> t.due_date = datetime.now()
        >>> t.status = TaskStatus.TODO
        >>> t.tags = ["blocker"]
        >>> t.updated_at = datetime.now()
        >>> calculate_task_score(t)
        68

    Notes:
        - DONE tasks lose 50 points to sink them to the bottom.
        - Overdue tasks get a +35 panic bonus.
        - Safely handles None tags and None updated_at (unlike original).
    """
    # Base score from priority level
    score = PRIORITY_WEIGHTS.get(task.priority, 0) * 10

    # --- Due date bonus ---
    # The closer the deadline, the more urgent it is
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:
            score += OVERDUE_BONUS        # Already late! 
        elif days_until_due == 0:
            score += DUE_TODAY_BONUS      # Due today! 
        elif days_until_due <= 2:
            score += DUE_SOON_BONUS       # Very soon
        elif days_until_due <= 7:
            score += DUE_THIS_WEEK_BONUS  # This week

    # --- Status penalty ---
    # Done tasks should sink to the bottom of the list
    if task.status == TaskStatus.DONE:
        score -= DONE_PENALTY
    elif task.status == TaskStatus.REVIEW:
        score -= REVIEW_PENALTY

    # --- Tag boost ---
    # Special keywords mean this task is extra important
    # SAFETY FIX: check task.tags is not None before iterating
    # (The original code would crash here if tags was None!)
    if task.tags and any(tag in IMPORTANT_TAGS for tag in task.tags):
        score += TAG_BOOST

    # --- Recency boost ---
    # Tasks updated recently might need finishing
    # SAFETY FIX: check task.updated_at is not None before calculating
    # (The original code would crash here if updated_at was None!)
    if task.updated_at:
        days_since_update = (datetime.now() - task.updated_at).days
        if days_since_update < RECENCY_WINDOW_DAYS:
            score += RECENCY_BOOST

    return score


def sort_tasks_by_importance(tasks: List[Task]) -> List[Task]:
    """Sort tasks by calculated importance score (highest first).

    Args:
        tasks: A list of Task objects.

    Returns:
        A new list with tasks ordered from highest score to lowest.
        The original list is not modified.

    Example:
        >>> tasks = [task_a, task_b, task_c]
        >>> sorted_tasks = sort_tasks_by_importance(tasks)
        >>> # sorted_tasks[0] is the most important task
    """
    # Pair each task with its score, then sort by score
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [
        task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)
    ]
    return sorted_tasks


def get_top_priority_tasks(tasks: List[Task], limit: int = 5) -> List[Task]:
    """Return the top N most important tasks.

    Args:
        tasks: A list of Task objects.
        limit: Maximum number of tasks to return. Default is 5.

    Returns:
        A list containing up to `limit` tasks, ordered by importance.

    Raises:
        ValueError: If `limit` is negative.

    Example:
        >>> all_tasks = [task1, task2, task3, task4, task5, task6]
        >>> top_3 = get_top_priority_tasks(all_tasks, limit=3)
        >>> len(top_3)
        3

    Notes:
        - If limit=0, returns an empty list.
        - If there are fewer tasks than the limit, returns all tasks.
    """
    # SAFETY FIX: validate limit is not negative
    # (The original code didn't check this!)
    if limit < 0:
        raise ValueError("limit must be 0 or positive")

    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
