---
name: visual-routine-prompting
description: |
  Provides accessible visual schedules for individuals with Down Syndrome. 
  Use when the user asks "what's next" or needs help with morning/daily routines.
  Do NOT use for medical diagnosis or suggesting therapy plans.
version: 1.0.0
---

# Visual Routine Prompting

## When to use
- When a user asks about their next routine task.
- When helping a user transition between daily activities (e.g., waking up, getting dressed).

## Workflow
1. **Identify Task:** Determine the next uncompleted routine item for the user.
2. **Format Component:** Call the local script `scripts/formatter.py` with the task name and a relevant icon name.
3. **Deliver UI:** Return the resulting A2UI JSON block to the user inside `
