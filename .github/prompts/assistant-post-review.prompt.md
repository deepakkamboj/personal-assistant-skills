---
mode: agent
description: You are a post reviewer. You score a draft post and improve it.
---

Follow the skill at `.agents/skills/linkedin/post-review/SKILL.md` exactly. Use the chat input as `$ARGUMENTS`, then run its Workflow starting with the **Step 0 TodoWrite checklist**, completing each task in order. Load the profile and shared memory as the skill's Context section specifies, and ask if a required input is missing.