---
name: grill-me
description: A relentless interview to sharpen a plan or design. Also questions implementation decisions during coding — the AI stops at every business rule to verify your understanding.
disable-model-invocation: false
---

# Grill Me — Planning & Implementation Review

Two modes. The AI detects which one to use based on context.

## Mode 1 — Planning (original Matt Pocock)

When the user is describing a plan, design, or idea BEFORE any code exists, run a `/grilling` session.

## Mode 2 — Implementation Review (Lucas Montano adaptation)

When code is being written or reviewed, question EVERY business-rule decision the AI makes. Stop at:

- Every `if`, `else`, `switch`, or conditional that encodes a business rule
- Every data validation or sanitization decision
- Every error-handling path that could affect user experience
- Every architectural choice (file structure, module boundaries, dependency direction)
- Every assumption about user behavior or system state

Rules for Mode 2:
- Ask ONE question at a time. Wait for my answer before continuing.
- If a *fact* can be found by exploring the codebase (existing code, config, tests), look it up rather than asking me.
- Present each decision with your RECOMMENDED answer — don't just ask open-ended.
- Focus ONLY on domain/business rules. Skip cosmetic or stylistic questions.
- After all branches resolved, summarize the decisions made before writing the final code.
- Do not implement until I confirm alignment.

Example Mode 2 flow:
```
AI writes: if (user.plan === 'premium') { ... }
AI asks: "This check only covers 'premium'. Should 'trial' and 'enterprise' users also get this feature? I recommend 'enterprise' yes, 'trial' no. What do you think?"

User: "Enterprise yes, trial no — correct."

AI continues, hits another branch:
AI asks: "For cancelled users, I'm soft-deleting data. Should we hard-delete after 30 days or keep indefinitely for compliance? I recommend 30-day retention then hard-delete."

User: "Keep 90 days, our compliance requires it."

...continues until all branches resolved...

AI: "Summary: (1) premium+enterprise get feature X, trial does not. (2) Cancelled users: soft-delete, hard-delete after 90 days. (3) ... Ready to implement?"

User: "Yes, go ahead."
```
