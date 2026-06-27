---
name: log-milestone
description: |
  Logs developmental achievements for individuals with Down Syndrome.
  Use when a parent says "He just did X for the first time" or "We reached a new milestone."
  Do NOT use for medical diagnosis.
version: 1.0.0
---

# Log Milestone

## When to use
- When a user reports a new developmental achievement (e.g., "She spoke her first word").
- When a user asks to record progress against a goal.

## Workflow
1. **Identify Milestone:** Extract the achievement and the date from the user's message.
2. **Retrieve Benchmarks:** Use the MCP tool `get_ds_benchmarks` to find the relevant developmental stage.
3. **Log Data:** Call the MCP tool `save_milestone` with the achievement and age-adjusted benchmark.
4. **Confirm Visually:** Return an A2UI `Card` with an "Achievement Unlocked" icon.

## Rules
- **Data Integrity:** Must confirm the specific date before logging.
- **Tone:** Use encouraging, strengths-based language.
Why this is the "Best Step":
Procedural Memory: You are giving the Progress Analyst procedural memory—the specific steps of how to log data, which the model lacks natively
.
MCP Integration: This skill introduces MCP tools (get_ds_benchmarks, save_milestone). Following your "Local First" requirement, we will implement these as stdio MCP servers in the next step, allowing the agent to query local JSON files as if they were a live database
.
A2UI Consistency: It continues the use of A2UI for visual confirmation, ensuring your interface remains accessible for the DS community
.