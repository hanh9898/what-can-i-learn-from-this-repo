# 08: Behaviour eval

**What to build:** One end-to-end eval, run through `skill-creator` both with the skill and against a no-skill baseline.

- **Source:** `mattpocock/skills`, pinned at a SHA.
- **Target:** a minimal skill-repo fixture with two planted answers:
  - A **gap** that must surface as a *match* lesson: no `disable-model-invocation` where it belongs, and reference not disclosed into separate files.
  - A **cargo-cult trap** that must land in "doesn't transfer": the source's TypeScript/npm tooling.
- **Checkpoints:** the eval prompt pre-answers both the lens checkpoint and the lesson choice, so the run reaches ticket creation.
- **Location:** evals and fixtures live at the repo root, outside the distributed skill folder. The `skill-creator` workspace is git-ignored.

**Blocked by:** 02, 03

**Status:** ready-for-agent

- [ ] Mechanical assertions pass, checked by script:
  - The report exists with the SHA.
  - Every lesson has forces and a label.
  - No *no* lesson appears in the brief.
  - Only the report and tickets were written.
  - The temp clone was removed.
  - There are no long source-code copies.
- [ ] Planted assertions pass: the gap appears as a *match* lesson and gets a ticket, and the trap appears under "doesn't transfer".
- [ ] The with-skill run passes every assertion, and the baseline fails at least the planted ones.
- [ ] The user reviewed the eval viewer output, and their feedback is recorded in this ticket's comments.
