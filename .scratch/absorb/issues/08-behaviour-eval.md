# 08: Behaviour eval

**What to build:** One end-to-end eval, run through `skill-creator` both with the skill and against a no-skill baseline.

- **Source:** `mattpocock/skills`, pinned at a SHA.
- **Target:** a minimal skill-repo fixture with two planted answers:
  - A **gap** that must surface as a *match* lesson: no `disable-model-invocation` where it belongs, and reference not disclosed into separate files.
  - A **cargo-cult trap** that must land in "doesn't transfer": the source's TypeScript/npm tooling.
- **Checkpoints:** the eval prompt pre-answers both the lens checkpoint and the lesson choice, so the run reaches ticket creation.
- **Location:** evals and fixtures live at the repo root, outside the distributed skill folder. The `skill-creator` workspace is git-ignored.

**Blocked by:** 02, 03

**Status:** resolved

- [x] Mechanical assertions pass, checked by script:
  - The report exists with the SHA.
  - Every lesson has forces and a label.
  - No *no* lesson appears in the brief.
  - Only the report and tickets were written.
  - The temp clone was removed.
  - There are no long source-code copies.
- [x] Planted assertions pass: the gap appears as a *match* lesson and gets a ticket, and the trap appears under "doesn't transfer".
- [x] The with-skill run passes every assertion, and the baseline fails at least the planted ones.
- [x] The user reviewed the eval viewer output, and their feedback is recorded in this ticket's comments.

## Comments

- **Design (2026-09-29)**: everything lives in `evals/absorb/`, and `evals/absorb/README.md` has the run steps.
  - The fixture `fixtures/skill-repo/` has two skills. `release-checklist` is run by hand but has no `disable-model-invocation`, and its 124-line `SKILL.md` inlines a 60-row rules table and a 40-term glossary. That is the planted **gap**. The repo has no package manager, so the source's npm/changesets tooling is the planted **trap**. The fixture never mentions `absorb` or this repo.
  - `evals.json` holds one eval in `skill-creator`'s schema. The prompt is natural language ("What can I learn from https://github.com/mattpocock/skills for this repo?"), so the baseline gets the same question. It pre-answers both checkpoints, and "adopt every lesson you rated a full match" makes the gap get a ticket without naming it.
  - `run.sh` copies the fixture into a git repo in the OS temp directory, outside this repo, so a run cannot read this repo's `CLAUDE.md` or tickets. `with_skill` adds `--plugin-dir <this repo>` and `without_skill` omits it. Both use `claude-sonnet-5` at medium effort. Before running, I checked that no `absorb` skill or plugin is installed elsewhere, so the baseline has none.
  - `check.py` grades [m1]–[m7] mechanically. A grader agent grades [p1]–[p3] following `skill-creator`'s `agents/grader.md`. `merge.py` joins them into `grading.json`, then `skill-creator` aggregates the benchmark and builds the static viewer.
- **"Pinned at a SHA"**: the skill always shallow-clones the source's current `HEAD`, so a URL@SHA pin cannot be honoured without new skill behaviour, which is out of scope here. Instead:
  - `evals.json` records the SHA the planted answers were designed against (`c55ee46`).
  - [m1] checks the report against the `HEAD` that `git ls-remote` returns at run time.
  - The README warns to recheck the planted answers if the source drifts.
- **Red/green**: here red is the no-skill baseline and green is the with-skill run on the same prompt, not a before/after edit.
- **Iteration 1 results**, after the review fixes to the grading scripts. The runs themselves came before those fixes.

  | Configuration | Passed | Time |
  |---|---|---|
  | with_skill | 10/10 | 366 s |
  | without_skill | 2/10 | 288 s |

  - **with_skill**: the report has the SHA, 16 permalinks, and a Coverage section. Both gap lessons are labelled *match*, each with a ticket in `.scratch/mattpocock-skills/`. The changesets/plugin tooling is under "Doesn't transfer". Only the report and 2 tickets were written.
  - **without_skill**: no report and no tickets. It edited `release-checklist/SKILL.md` and `README.md` directly and added two reference files. It never added `disable-model-invocation`; it only reworded the description. It fails [p1]–[p3], as criterion 3 requires, plus [m1]–[m4] and [m7].
- **Code review** (fixed point `83a4c32`):
  - Standards: 10 findings.
    - Fixed:
      - English-only label and brief parsing gave false failures on Vietnamese output. Labels are now matched by value, and the brief's parts are split by their bold labels in any language.
      - A case-sensitive label match.
      - [m7] failed on negated mentions and passed on zero tickets.
      - [m4] failed on non-ASCII paths. Fixed with `core.quotepath=off`.
      - [m7] read each ticket twice.
      - Short variable names.
      - `merge.py` silently merged without `planted.json`.
      - `run.sh` leaked its temp target on an early exit. Fixed with a `trap`.
      - `run.sh` did not validate the configuration argument.
      - The source URL was duplicated between `run.sh` and `evals.json`.
      - stderr was mixed into the graded final message.
    - Skipped:
      - Keying assertions by their `[m1]` text prefix: the ids are part of the viewer-facing text by design.
      - Forcing English output in the prompt: the author's real environment answers in Vietnamese, and the eval should cover that.
  - Spec: 3 findings.
    - The pin is not honoured. Recorded above.
    - [m7] passed vacuously on the baseline. Fixed: it now needs at least one ticket.
    - `benchmark.md` was mojibake. Fixed by regenerating with `PYTHONUTF8=1`. Its `runs_per_configuration: 3` is `skill-creator`'s default label, not our data: there is one run per configuration.
  - The rewritten `run.sh` passed `bash -n`. The two recorded runs came from the version before the review, so the new `run.sh` has not been executed end to end yet.
- **Grader's eval feedback**: the baseline also rewrote the fixture README's "Where it hurts" section, which erases the problem it just fixed. No assertion checks this. It is a candidate for iteration 2.
- **User review (2026-09-29, criterion 4)**: the user reviewed `evals/absorb-workspace/iteration-1/review.html` and judged the eval a pass. They asked to add the grader's README assertion. Added as [m8]: the target's README, including its "Where it hurts" section, is unchanged. Grading the recorded runs again with it gives 11/11 for with_skill and 2/11 for without_skill (it rewrote the README). The new `run.sh` will exercise it on the next live run.
