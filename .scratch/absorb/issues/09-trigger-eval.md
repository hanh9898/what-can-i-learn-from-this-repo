# 09: Trigger eval and description optimisation

**What to build:** Run about 10 should-trigger and should-not-trigger queries through `skill-creator`'s description loop. The set includes these near-misses: "summarise this repo", "onboard me into this repo", "review my PR", "compare two libraries" and "research API X". The description with the best held-out score replaces the skill's current one.

**Blocked by:** 08

**Status:** ready-for-agent

- [ ] The user reviewed the query set before it ran.
- [ ] The description loop ran on the model powering the session, and its report is recorded in this ticket's comments.
- [ ] The chosen description triggers on every should-trigger query and on no near-miss in the held-out set. Any misses are recorded with a reason.
- [ ] The new description still passes the pointer rules in `CODING_STANDARDS.md`.
