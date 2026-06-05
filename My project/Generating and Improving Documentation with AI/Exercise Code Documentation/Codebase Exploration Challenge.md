# Exercise: Code Documentation
## Python
---

##  Contents of This Submission

| File | What It Is |
|------|-----------|
| [`original_code.py`](original_code.py) | The starter code exactly as I found it in the repo |
| [`prompt1_documentation.md`](prompt1_documentation.md) | Comprehensive docs generated using Prompt 1 |
| [`prompt2_analysis.md`](prompt2_analysis.md) | Intent, logic, edge cases & improvements from Prompt 2 |
| [`final_combined.py`](final_combined.py) | My polished version combining the best of both prompts |
| `README.md` | This file — overview and what I learned |

---

##  Why I Chose `task_priority.py`

I picked this file because it had the most interesting logic to document. It calculates a "priority score" for tasks using multiple factors (due dates, status, tags, recency) and then sorts them. At first glance it looked simple, but once I dug in I found edge cases, magic numbers, and potential crashes that made it way more complex than it seemed.

---

##  What I Learned

### 1. Which parts of the documentation were most challenging for the AI?

The AI was great at writing basic docstrings, but it struggled with:

- **Edge cases:** It didn't automatically notice that `task.tags` or `task.updated_at` could be `None` and would crash the code. I had to actually **run the code** with a task that had `None` tags to discover this bug. Then I had to go back and tell the AI "hey, check for `None` values too." It missed it on the first try.

- **Magic numbers:** The AI described what the numbers did (like "35 is for overdue") but didn't suggest moving them to named constants. I only got that suggestion when I specifically asked for "potential improvements" in Prompt 2.

- **Real-world messiness:** The AI wrote perfect-looking examples, but they assumed perfect data. Real data has missing fields, wrong types, etc. The AI didn't warn about that until I pushed it.

### 2. What additional information did I need to provide in my prompts?

- I had to **specify the docstring style** I wanted. At first the AI gave me a generic format, but I wanted Google-style docstrings with specific sections (Args, Returns, Raises, Example, Notes). I had to list those out explicitly.

- I had to mention that this is **starter code that is intentionally messy**. The AI initially just described the code as-is. When I told it "this is intentionally unoptimized starter code, look for bugs and improvements," it actually started finding issues.

- For Prompt 2, I had to ask specifically about **"assumptions and edge cases"** and **"inline comments."** If I just said "explain this code," I got a high-level summary but not the deep dive.

- I also had to **test the code myself**! The AI can suggest things, but I won't know if they're right until I actually run it. I found the `None` crash by testing, not by reading AI output.

### 3. How would I use this approach in my own projects?

- **Two-pass method:** I'll definitely use Prompt 1 first (get the "reference manual" docs) and then Prompt 2 (get the "code review" insights). Doing both gives way better results than just one.

- **Always test:** The AI can sound very confident about wrong things. I learned to never trust AI output without running it. The `None` crash was a good lesson — the AI said the code "handles edge cases" but it clearly didn't.

- **Save prompt templates:** I wrote down my two prompts in a notes file so next time I need to document code, I can just swap in the new function and re-run them. Saves a ton of time.

- **Ask about the weird stuff:** The AI is good at happy-path docs but misses the weird edge cases. I need to explicitly ask about `None` values, empty lists, negative numbers, etc. every time.

- **Combine, don't just copy:** The AI gave me drafts, but I had to edit them, add my own testing notes, and combine the best parts from both prompts. The final version is better than either prompt's output alone.

**Overall:** AI is a great **helper** for documentation, but it's not a replacement for actually understanding the code and testing it yourself. The AI gives you a head start, but you still need to bring your own brain! 

---

##  How to Run the Final Code

```bash
# The final version uses type hints and requires Python 3.9+
python final_combined.py
```

> Note: `final_combined.py` is a module file (it defines functions). To actually test it, you'd need the `models.py` file from the starter repo too. The documentation and code structure are the main deliverables for this exercise.
