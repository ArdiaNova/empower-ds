---
name: provide-encouragement
description: |
  Provides positive reinforcement and celebratory feedback.
  Use when a user achieves a milestone (reported by the Analyst) or needs emotional support.
  Do NOT use for clinical advice or medical recommendations.
version: 1.1.0
---

# Provide Encouragement

## Workflow
1. **Analyze Context:** Review the milestone achievement or current routine state.
2. **Select Vibe:** Choose a celebration theme (for milestones) or a support theme.
3. **Format UI:** Call the local script `scripts/generator.py` with a headline and message.
4. **Deliver UI:** Return the resulting A2UI JSON block inside `