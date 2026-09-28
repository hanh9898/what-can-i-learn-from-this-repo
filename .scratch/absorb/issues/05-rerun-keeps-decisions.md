# 05: Re-run keeps prior decisions

**What to build:** When the target already has a report for the same source, the skill:

- Loads the report's decisions before anything else.
- Never re-asks about a lesson that was already decided.
- Shows only lessons that are new, or whose forces changed in the target.
- Updates the SHA and the report in place.

**Blocked by:** 01

**Status:** resolved

- [x] A second run on the same source shows no lesson the user already adopted or rejected, unless that lesson's label changed.
- [x] The report keeps every earlier decision and records the new SHA.
- [x] A lesson whose label changed is shown with its old decision and the reason it changed.

## Comments

- **Design**: three edits, all in this ticket's zone of `skills/absorb/SKILL.md`.
  - `## 0. Prior report` finds `docs/lessons/<slug>.md` by step 2's slug rule. It loads the SHA and each lesson's name, label and, for *match*/*partial*, the decision. It hands the names to step 3, so a rediscovered practice keeps its name. Lessons are matched across runs by **Name**, which `lesson-format.md` already says is reused "in any later run".
  - Brief bullet **Prior decisions**: a prior lesson with an unchanged label only appears in a count. A lesson whose label changed is listed there, whatever its new label, with its old label and decision, its new label, and the force that changed, and it is decided again.
  - The last sentence of step 6: the report is updated in place with the new SHA and date, keeps every earlier lesson and decision (including lessons not found again), and keeps a changed lesson's old label and decision beside the new ones.
- **Smoke runs** (2026-09-29). Source: the local `mattpocock/skills` clone at `2aecca1`. Target: a temp clone of this repo at `a706093`. Checkpoints were pre-answered: accept the lens; adopt the first lesson asked about and reject the rest.
  - **Setup (run A, base skill, first run):** 5 brief lessons (2 adopted, 3 rejected) and 4 *no* lessons. The report was committed in the target. Then the SHA was set to a fake older one (`0b1c2d3…`, date 2026-09-01), because the clone is shallow. The stored label of "Local dev symlink script" was also flipped from *partial* to *match*.
  - **Red (run B, base skill copy):** 7 `## Pause` headings: the lens, plus one adopt/reject pause per lesson for 6 lessons, all 5 previously decided lessons included. "AGENTS.md as a one-line pointer" went from Adopted to Rejected with its label unchanged, so an earlier decision was lost. No old decision was shown for any lesson. Red on criteria 1–3. The SHA was updated.
  - **Green (run C, changed skill, same target as B):** 2 pauses (Lens, Brief). **Prior decisions** matched all 9 prior lessons by name with unchanged labels and showed them only as a count. The brief asked only about 1 new lesson. `git diff`: the SHA changed to `2aecca1`, every earlier `Decision` line survived, and 2 new lessons were appended. `git status --porcelain`: ` M docs/lessons/mattpocock.md` only. The planted label flip was not re-judged: the runner kept the stored *match*. So criterion 3 was not exercised by this run.
  - **Green (run D, skill after review fixes).** Same prior report. The target's forces were then genuinely changed in a commit:
    - Ticket 07 is `wontfix`, and the spec drops Codex.
    - A new ticket 10 describes recurring em-dash disputes.

    Results:
    - 2 pauses (Lens, Brief).
    - **Prior decisions** counted 4 unchanged lessons.
    - It listed 2 changed lessons, each with its old decision and the force that changed:
      - "AGENTS.md as a one-line pointer": *match*/Adopted became *no*, because Codex was dropped.
      - "Repo-wide no-em-dash prose rule": *no*/no decision became *match*, because of ticket 10.
    - The user was asked about exactly those 2 plus 1 new lesson.
    - The report was updated in place:
      - The SHA moved from `0b1c2d3…` to `2aecca1`, and the date to 2026-09-29.
      - All 4 unchanged decisions are kept verbatim.
      - Both changed lessons carry a "Changed since last run" line with the old label and decision.
    - `git status --porcelain` shows only ` M docs/lessons/mattpocock.md`.

    Green on criteria 1–3.
  - Caveat: the target is this repo, so the runners could read this ticket. Run D's prompt told the runner to take behaviour only from the skill and to re-judge every label.
- **`claude plugin validate .`**: passed. No frontmatter was touched.
- **Code review** (fixed point `a706093`):
  - Standards: 4 findings.
    - Single source of truth: step 5 and step 6 both restated the carry-forward rule. Fixed: the step 6 sentence now covers only what the file keeps and points at **Prior decisions** for changed lessons.
    - Co-location: step 0 instructs step 3 to reuse names, but step 3 says nothing. Skipped: step 3 is ticket 04's zone. Hand-off below. Runs C and D show that the step-0 hand-over is enough: every prior lesson was matched by name.
    - Completion criterion (hard): step 6's **Done when** does not check the carried-forward lessons. Skipped: ticket 03's zone. Hand-off below.
    - Data Clumps (judgement): "name, label, decision" travel together, and `lesson-format.md` has no Decision field. Partly fixed: step 0 now says a decision exists only for *match*/*partial*. No new term was coined.
  - Spec: 2 findings.
    - The **Lessons** bullet still reads as unfiltered, so the exclusion sits only in **Prior decisions**. Skipped: that bullet is outside this zone. The new bullet sits directly under it. Hand-off below.
    - Name matching depends on step 3, which does not consume the names. This is the same issue as Standards finding 2, and was skipped with the same hand-off.
    - No scope creep was reported.
- **Hand-offs** (changes outside this zone):
  - **04 (step 3):** add to Assimilate "a lesson for a practice the prior report names reuses that name", so a subagent-per-dimension sweep, where subagents never see step 0, still gets the prior names in its prompt.
  - **03 (step 6):** extend the **Done when** with "and, when step 0 loaded a report, keeps every lesson and decision it held".
  - **Step 5 Lessons bullet (no zone):** consider "the new *match* and *partial* lessons only" so that the exclusion is stated where the list is defined.
  - **02 (description, README `## Use`):** may mention that a re-run keeps earlier decisions. Not required.
- **Open, from run D's ambiguities (not blocking the criteria):**
  - Whether an unchanged prior *no* lesson is counted under **Prior decisions**, **Not transferred**, or both.
  - Where a changed lesson goes in the report when its new label is *no*. Run D put it under "Doesn't transfer" with a changed-since note.
  - Whether the report should keep a history of earlier SHAs. Currently only the latest SHA is kept.
