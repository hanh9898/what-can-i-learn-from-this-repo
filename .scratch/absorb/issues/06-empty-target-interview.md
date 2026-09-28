# 06: Empty or thin target — interview for the lens

**What to build:** When the target has too little to infer a lens from (an empty folder, or only a README), the skill interviews the user about their goals and pain points instead of inferring. It then continues with the lens the interview produced.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] In an empty target, the skill asks about goals and pain points before it reads the source.
- [ ] In a populated target, the skill infers the lens and does not interview.
- [ ] The report records the lens the interview produced.

## Comments

- **Seam and expected pauses (written before any run)**: the seam is the smoke run from the wave 1 common rules. A subagent follows `SKILL.md` literally, playing a user persona with a planted pain point (the made-up tool `Quillmark`). It logs what it shows the user to `transcript.md`, every file it reads to `reads.md` in order, and ambiguities to `ambiguities.md`. Expected `## Pause` headings:
  - Empty target, red (base skill): lens, then brief. No interview. `Quillmark` absent from the report.
  - Empty target, green: interview, then lens, then brief. No source path in `reads.md` before the interview pause. `Quillmark` in the report's **Lens** section.
  - README-only target, green: the same as the green empty target.
  - Populated target (a copy of this repo), green: lens, then brief. No interview. Its "before" state is ticket 01's smoke run, which stopped at the lens and the brief.
- **Smoke runs (2026-09-29)**: the source was the local clone of `mattpocock/skills` at `2aecca1`. Each target was a `git init`'d folder under the ticket's temp directory. Red used the skill copied from `a706093`, green used this branch. All four runs got the same runner prompt; only the skill path and the target path differed.
  - **Red, empty target**: pauses were `1. Lens` (corrections) and `5. Checkpoint`. There was no interview. The lens read "stack, size, existing conventions, and pain points cannot be determined", so all 14 lessons came out *no* and the brief was empty. The report's **Lens** section had no `Quillmark`. The runner logged it as an ambiguity: "the skill never instructs asking the user about goals/stack/pain points". Red on criteria 1 and 3.
  - **Green, empty target**: pauses were `1. Lens` (interview on goals and pain points), `1. Lens` (corrections) and `5. Checkpoint`. In `reads.md` the first source line comes after the `--- Pause 1 ---` marker. The report's **Lens** section records both planted pain points, `Quillmark` included. The brief held 4 lessons. Green on criteria 1 and 3.
  - **Green, README-only target**: the same three pauses, and the report's **Lens** section has `Quillmark`. One deviation: the runner listed the source's root directory before the interview, but opened no source file until after it. The criteria name only the empty target, and step 1 still comes before step 2, so I left the wording as is.
  - **Green, populated target** (a copy of this repo at `a706093` without `.scratch/`): pauses were `1. Lens` (corrections) and `5. Checkpoint`. There was no interview and no `Quillmark`. The runner judged the target not thin because it has agent config and manifests. Green on criterion 2. Ticket 01's smoke run is the "before" for this case.
  - **Write scope**: in all four targets, `git status --porcelain -uall` listed only `docs/lessons/mattpocock.md`.
  - The runners logged two ambiguities, and both are expected. One folded a stack question into the interview. All of them counted the interview and the lens corrections as two separate pauses.
