# 05: Re-run keeps prior decisions

**What to build:** When the target already has a report for the same source, the skill:

- Loads the report's decisions before anything else.
- Never re-asks about a lesson that was already decided.
- Shows only lessons that are new, or whose forces changed in the target.
- Updates the SHA and the report in place.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] A second run on the same source shows no lesson the user already adopted or rejected, unless that lesson's label changed.
- [ ] The report keeps every earlier decision and records the new SHA.
- [ ] A lesson whose label changed is shown with its old decision and the reason it changed.
