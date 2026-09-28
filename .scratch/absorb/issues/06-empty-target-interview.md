# 06: Empty or thin target — interview for the lens

**What to build:** When the target has too little to infer a lens from (an empty folder, or only a README), the skill interviews the user about their goals and pain points instead of inferring. It then continues with the lens the interview produced.

**Blocked by:** 01

**Status:** resolved

- [x] In an empty target, the skill asks about goals and pain points before it reads the source.
- [x] In a populated target, the skill infers the lens and does not interview.
- [x] The report records the lens the interview produced.

## Comments

- **Seam and expected pauses (written before any run)**: the seam is the smoke run from the wave 1 common rules. A subagent follows `SKILL.md` literally, playing a user persona with a planted pain point (the made-up tool `Quillmark`). It logs what it shows the user to `transcript.md`, every file it reads to `reads.md` in order, and ambiguities to `ambiguities.md`. Expected `## Pause` headings:
  - Empty target, red (base skill): lens, then brief. No interview. `Quillmark` absent from the report.
  - Empty target, green: interview, then lens, then brief. No source path in `reads.md` before the interview pause. `Quillmark` in the report's **Lens** section.
  - README-only target, green: the same as the green empty target.
  - Populated target (a copy of this repo), green: lens, then brief. No interview. Its "before" state is ticket 01's smoke run, which stopped at the lens and the brief.
- **Smoke runs (2026-09-29)**: the source was the local clone of `mattpocock/skills` at `2aecca1`. Each target was a `git init`'d folder under the ticket's temp directory. Red used the skill copied from `a706093`, green used this branch's first wording (commit `501fd3c`), before the review fixes below. All four runs got the same runner prompt; only the skill path and the target path differed.
  - **Red, empty target**: pauses were `1. Lens` (corrections) and `5. Checkpoint`. There was no interview. The lens read "stack, size, existing conventions, and pain points cannot be determined", so all 14 lessons came out *no* and the brief was empty. The report's **Lens** section had no `Quillmark`. The runner logged it as an ambiguity: "the skill never instructs asking the user about goals/stack/pain points". Red on criteria 1 and 3.
  - **Green, empty target**: pauses were `1. Lens` (interview on goals and pain points), `1. Lens` (corrections) and `5. Checkpoint`. In `reads.md` the first source line comes after the `--- Pause 1 ---` marker. The report's **Lens** section records both planted pain points, `Quillmark` included. The brief held 4 lessons. Green on criteria 1 and 3.
  - **Green, README-only target**: the same three pauses, and the report's **Lens** section has `Quillmark`. One deviation: the runner listed the source's root directory before the interview, but opened no source file until after it. The criteria name only the empty target. The rerun on the final wording, below, did not repeat it.
  - **Green, populated target** (a copy of this repo at `a706093` without `.scratch/`): pauses were `1. Lens` (corrections) and `5. Checkpoint`. There was no interview and no `Quillmark`. The runner judged the target not thin because it has agent config and manifests. Green on criterion 2. Ticket 01's smoke run is the "before" for this case.
  - **Write scope**: in all four targets, `git status --porcelain -uall` listed only `docs/lessons/mattpocock.md`.
  - The runners logged two ambiguities, and both are expected. One folded a stack question into the interview. All of them counted the interview and the lens corrections as two separate pauses.
- **Code review** (fixed point `a706093`, spec this ticket plus `spec.md`, standard `CODING_STANDARDS.md`):
  - Standards: 4 findings, all judgement calls, none hard.
    - Leading words: the interview asked about "goals and pain points", which skipped the lens's stack slot and renamed "where it hurts". Fixed: it now asks about goals, planned stack, and where it hurts.
    - Leading words: "thin" was defined as "no code, manifest or agent config", which would also flag a target holding a glossary or ADRs. Fixed: thin now means no code and none of the lens files beyond a README.
    - "Interview the user instead" clashed with building the lens from the answers "and whatever the target holds". Fixed: dropped "instead".
    - Branch test: the thin branch sits inline, not behind a pointer. Skipped, because two sentences cost less inline than a disclosed file would.
  - Spec: 1 finding. The ticket's status, checkboxes and review record were not updated yet. Fixed in this commit. No scope creep. Criterion 3 is met by the existing step 6 **Lens** bullet ("as the user accepted it"), so step 6 is unchanged.
- **Green reruns after the review fixes (2026-09-29)**: all three green targets were reset and run again against the final wording, with the same prompt.
  - Empty target: pauses were `1. Lens` (interview on goals, stack, and pain points), `1. Lens` (corrections) and `5. Checkpoint`. The first source line in `reads.md` comes after `--- Pause 1 ---`. The report's **Lens** section has `Quillmark`.
  - README-only target: the same three pauses and the same ordering. This time the source was not listed before the interview. The report's **Lens** section has `Quillmark`.
  - Populated target: pauses were `Lens` (corrections) and `Checkpoint`. There was no interview and no `Quillmark`.
  - In every target, `git status --porcelain -uall` listed only `docs/lessons/mattpocock.md`. The source clone's `git status --porcelain` stayed empty.
- **Open**: none for this ticket. Two notes for later tickets:
  - The interview and the lens corrections are two stops in step 1. That is inside the spec's deliberate early-lens exception, but ticket 08's eval should pre-answer both.
  - The report's **Lens** section does not say that the lens came from an interview. The criteria do not ask for this. If it is wanted, it is a change to the step 6 **Lens** bullet, which is outside this ticket's zone.
