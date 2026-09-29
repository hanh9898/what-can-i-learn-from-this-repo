# 09: Trigger eval and description optimisation

**What to build:** Run about 10 should-trigger and should-not-trigger queries through `skill-creator`'s description loop. The set includes these near-misses: "summarise this repo", "onboard me into this repo", "review my PR", "compare two libraries" and "research API X". The description with the best held-out score replaces the skill's current one.

**Blocked by:** 08

**Status:** ready-for-human

- [x] The user reviewed the query set before it ran.
- [ ] The description loop ran on the model powering the session, and its report is recorded in this ticket's comments.
- [x] The chosen description triggers on every should-trigger query and on no near-miss in the held-out set. Any misses are recorded with a reason.
- [x] The new description still passes the pointer rules in `CODING_STANDARDS.md`.

## Comments

- **Query set (2026-09-29)**: `evals/absorb/trigger/trigger-eval.json`, 10 queries, reviewed and approved by the user before any run.
  - Should trigger:
    - "what can I learn from next.js for this project"
    - a Vietnamese "what in mattpocock/skills is worth applying here"
    - a local clone with "adopt vs cargo cult"
    - "what's worth borrowing from shadcn-ui"
    - "compare our testing and CI against ruff"
  - Should not trigger (near-misses):
    - summarise a repo
    - onboard me into this repo
    - review my PR
    - compare zod and valibot
    - research the GitHub API rate limits
- **Model**: `claude-sonnet-5`, chosen by the user. Headless runs on the session's model, `claude-opus-5-5`, had been refused by the `reasoning_extraction` safeguard. So criterion 2's "model powering the session" is not met exactly: the loop ran on Sonnet 5.
- **Windows fixes**:
  - `trigger/sitecustomize.py`: `skill-creator`'s `run_eval` calls `select()` on a subprocess pipe, which Windows rejects, and every query then counted as "not triggered". The shim reports the pipe as ready, so reads block instead.
  - One worker instead of 10: parallel runs of the same query each drop an identical copy of the skill into the shared `.claude/commands`, and the model can pick another run's copy.
  - A 120 s timeout instead of 30 s, because a cold `claude` start here takes longer than 30 s.
- **The description loop** (`run.sh <dir> loop`, 5 iterations, 40% held out) ran twice, and both times the measurement was invalid.
  - The first run used parallel workers and hit the collision above.
  - The second run was serialised. Every run was still killed about 4 s in, before the model replied: the session logs hold only the user message. So the loop recorded roughly 0% recall for every description it tried, including the current one. For the current description, "Best score: 2/4 (iteration 1)" came from the near-misses alone.
  - The loop's proposals, such as "Adopt practices from another codebase…" and "Trigger when a user points at another codebase…", were scored against that broken measurement, so none is evidence of a better description.
  - I have not found why the loop's runs die when `run_eval`'s identical runs do not.
- **Direct measurement**: `run_eval` on the current description, 3 runs per query, 1 worker, 120 s timeout. **30/30**: every should-trigger query fired 3/3, and every near-miss fired 0/3. Criterion 3 is therefore met by the current description, and the description is unchanged.
- **Pointer rules** (criterion 4), checked on the unchanged description:
  - It leads with the trigger question.
  - It names one trigger branch.
  - It does not restate the body.
  - It advertises only behaviour that exists: GitHub URL or local path.
- **Open, for the user**: criterion 2 is not met. The loop's report is recorded above, but it ran on Sonnet 5, and its measurement is invalid on this machine. The user decides between two options:
  - accept the direct `run_eval` measurement as the evidence and close the ticket;
  - debug the loop further, or run it on another machine.
- **Code review** (fixed point `c65e38e`):
  - Standards: 3 findings.
    - The Windows shim replaced `select()` for every caller and always claimed readiness, so a truly silent child could block forever. Fixed: the shim now polls `PeekNamedPipe` until data arrives, the pipe closes, or the timeout passes, and it hands sockets to the real `select()`. A unit check confirmed the timeout, data and EOF paths. A 2-query `run_eval` run gave 2/2 triggers and 0/2 for the near-miss.
    - Through `PYTHONPATH`, the shim reaches every Python process the eval starts. Fixed by the same change: an inheriting process now only ever gets correct `select()` behaviour.
    - A `.pyc` file was committed. Fixed: removed, and `__pycache__/` is now in `.gitignore`.
  - Spec: 3 findings.
    - Criterion 2 is correctly left open. No change.
    - Criterion 3 cites a full-set `run_eval` rather than the loop's held-out split. Noted: the full-set measurement covers the held-out queries too, and every one of the 10 queries passed 3/3.
    - Criterion 4's "advertises only existing behaviour" check comes from ticket 01's review, not from a named pointer rule. Noted, and the other three bullets are the pointer rules.
