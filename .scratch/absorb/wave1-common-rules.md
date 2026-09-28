# Common rules for wave 1 (tickets 02, 03, 04, 05, 06, 07)

## Graph
`00✓ → 01✓ → {02, 03, 04, 05, 06, 07} → 08 (needs 02, 03) → 09`

| Ticket | Status | Blocked by | Wave |
|---|---|---|---|
| 00 | resolved | - | done before waves |
| 01 | resolved | 00 | done before waves |
| 02 | ready-for-agent | 01 | 1 |
| 03 | ready-for-agent | 01 | 1 |
| 04 | ready-for-agent | 01 | 1 |
| 05 | ready-for-agent | 01 | 1 |
| 06 | ready-for-agent | 01 | 1 |
| 07 | ready-for-agent | 01 | 1 |
| 08 | ready-for-agent | 02, 03 | 2 |
| 09 | ready-for-agent | 08 | 3 |

## Context
- Your worktree branches off `main` at the base commit named in your prompt. That branch already contains tickets 00 and 01, plus a prefactor that turned the checkpoint's brief into one bullet per part. Run `git branch --show-current` before every commit.
- Before you start, read:
  - `.scratch/absorb/spec.md`
  - `CODING_STANDARDS.md` (it is the review standard for every file in `skills/absorb/`)
  - your ticket
  - the `## Comments` of ticket 01, which hold the smoke-run evidence and hand-offs to 02 and 06
- Five other agents are working the rest of this wave in parallel, on other branches. Work only on your own ticket.
- Do not end your turn while work you started is still running in the background, such as a smoke-run subagent or the review sub-agents that `mattpocock-skills:code-review` launches. Wait for it inside the same turn. Paseo sends no finish notification for a turn you start on your own afterwards, so your "finished" report must mean the work is done.

## Existing interfaces to reuse
- **The skill's step headings**: `## 1. Lens`, `## 2. Acquire`, `## 3. Assimilate`, `## 4. Transform`, `## 5. Checkpoint`, `## 6. Exploit`. Each ends on a `**Done when**` line. Keep this shape; a new step gets its own numbered heading and its own `**Done when**`.
- **The brief's parts**: a bullet list in step 5 (**Lessons**, **Not transferred**, **Report**). A ticket that adds to the brief adds its own bullet.
- **The report's sections**: a bullet list in step 6 (**Source**, **Lens**, **Lessons**, **Doesn't transfer, and why**).
- **Lesson fields and labels**: live only in `skills/absorb/lesson-format.md`. Point at them; do not restate them.

## File zones

| Ticket | Owns |
|---|---|
| 02 | Frontmatter `description` and `argument-hint`, step 2 Acquire and its slug rule, the "The source is read-only" sentence in the intro, one bullet in the brief (permalinks), the **Source** bullet of the report, README `## Use` |
| 03 | Step 6 Exploit (except one sentence reserved for 05), the intro sentence "The only file this skill writes in the target is the report", one bullet in the brief (where tickets go), any new disclosed file for ticket format |
| 04 | Step 3 Assimilate, `dimensions.md`, one bullet in the brief (coverage note) |
| 05 | A new step before Lens (renumber nothing else: call it `## 0. Prior report`), one bullet in the brief (prior decisions), one sentence at the end of step 6 on updating an existing report in place |
| 06 | Step 1 Lens |
| 07 | `skills/absorb/agents/openai.yaml` (new), README `## Install (Codex)` (new section after `## Install (Claude Code)`) |

- **Shared files** (`SKILL.md`, `README.md`): edit only your own zone. Add your own lines without reordering existing ones.
- A ticket that genuinely needs a change outside its zone writes the needed change into its ticket comments instead of making it.
- `plugin.json` and `marketplace.json` are nobody's zone in this wave.

## Traps already hit
- **Smoke run is the test.** There is no code, so the red/green loop of `mattpocock-skills:tdd` is a smoke run. You dispatch a subagent that follows `skills/absorb/SKILL.md` literally, as ticket 01 did.
  - Pre-answer each checkpoint in its prompt.
  - Have it append everything it would show the user to a `transcript.md`, and every ambiguity to an `ambiguities.md`, both outside the target.
  - Run it once before your change, where it is **red** on your ticket's criteria, and once after, where it is **green**. Record both in your ticket's comments.
  - **How to check:** the transcript's `## Pause` headings match the checkpoints you expect.
- **An ambiguity pause is not a skill stop.** In ticket 01 the runner recorded "Pause 2" to flag an ambiguity. Tell your runner to log ambiguities only in `ambiguities.md`, not as pauses.
  - **How to check:** every `## Pause` heading in the transcript names a checkpoint the skill defines.
- **Write scope.** The target of a smoke run must be a git repo, so any stray write shows up.
  - **How to check:** `git -C <target> status --porcelain` lists only what your ticket allows.
- **The description oversold.** Ticket 01's review caught a description that advertised GitHub URLs before they worked. Describe only behaviour that exists on your branch, and keep the leading word (the trigger question) first.
  - **How to check:** reread the frontmatter against the steps.
- **The source is a local clone.** A local clone of `mattpocock/skills` is at `C:\Users\HBLAB_OPMS\.claude\plugins\marketplaces\mattpocock`. Read it and never write to it. Ticket 02 also needs a real GitHub URL, which is `https://github.com/mattpocock/skills`.
- **LF/CRLF.** "LF will be replaced by CRLF" warnings on `git add` are harmless. Ignore them.

## Acceptance criteria are the contract
- A trap above, or an instruction an earlier ticket left in its comments, is guidance. Your ticket's acceptance criteria are the contract.
- On conflict, follow the criteria and write the discrepancy and its reason in your ticket's comments. Do not stop to ask.
- If the criteria themselves look wrong, stop that part, write the evidence in your ticket's comments, and move the ticket to `ready-for-human`. Never rewrite the criteria.
- **Ticket 07 only:** this machine has no Codex CLI and Paseo reports the Codex provider unavailable, so criterion 3 (a manual smoke run on Codex) is for a human. Do criteria 1–2, leave criterion 3 unchecked, set `**Status:** ready-for-human`, and state in the comments exactly what the human must run.

## Resources
- Your private resources are listed in your prompt: one temp directory. Put smoke-run targets, transcripts and clones under it and nowhere else.
- Shared resources, read-only: the local `mattpocock/skills` clone above, and the integration checkout at `D:\what-can-i-learn-from-this-repo`, where this file lives.

## Repo and user rules
- **Language:** commit messages, ticket comments and skill text are in English.
- **Commits:** every commit message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Never push; never commit to `main`.
- **Accepted verification:** the smoke run above. Also run `claude plugin validate .` after touching any manifest or skill frontmatter.
- **Evidence standards:** none declared.

## Done when:
- Commit to your branch. The orchestrator merges.
- Before the last commit:
  - Run `/mattpocock-skills:code-review` with your base commit as the fixed point, your ticket as the spec, and `CODING_STANDARDS.md` as the standard.
  - Fix the findings.
  - Write the number of findings per axis, and the outcome of each, into the ticket's comments.
- Change the ticket status: `resolved` if fully done, `ready-for-human` for the part a human must do. In the comments, write what you verified, with the red and green smoke-run evidence, and what remains open. Tick only the criteria you verified.
- Clean up your temp directory. State the reason for anything you keep.
- Report back:
  - a design summary
  - files touched
  - how you verified, with evidence
  - work not done or still in doubt
  - decisions the user must make
