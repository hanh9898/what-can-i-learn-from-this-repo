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

## Wave agents

| Ticket | Agent id | Workspace id | Branch | Base commit | Private resources | Cleaned |
|---|---|---|---|---|---|---|
| 02 | f83f7151-5d9c-4b1b-ab9f-9bf59663ef29 | wks_0b767950a8f023bf | wave1/02-github-url-source | a706093 | C:\Users\HBLAB_~1\AppData\Local\Temp\absorb-wave1-02 | [x] |
| 03 | 4ffda535-26f4-4d62-979d-f052fe062dec | wks_c1c6b5f2a31f12cc | wave1/03-exploit-to-tickets | a706093 | C:\Users\HBLAB_~1\AppData\Local\Temp\absorb-wave1-03 | [x] |
| 04 | b4cd01e4-6dae-4c6a-a3d9-498817a7220d | wks_b1e4a555810d1f2d | wave1/04-subagent-per-dimension | a706093 | C:\Users\HBLAB_~1\AppData\Local\Temp\absorb-wave1-04 | [x] |
| 05 | 687c7f67-4ef7-430f-8213-d74258c3822c | wks_2525238762124371 | wave1/05-rerun-keeps-decisions | a706093 | C:\Users\HBLAB_~1\AppData\Local\Temp\absorb-wave1-05 | [x] |
| 06 | 4a25ce50-8845-47c6-9910-3620a981279e | wks_9790916ecdc8d389 | wave1/06-empty-target-interview | a706093 | C:\Users\HBLAB_~1\AppData\Local\Temp\absorb-wave1-06 | [x] |
| 07 | e0ca5fd9-ef07-424d-bc39-043dacfeb290 | wks_0ce7c3d8c496f462 | wave1/07-codex-support | a706093 | C:\Users\HBLAB_~1\AppData\Local\Temp\absorb-wave1-07 | [x] |

## Review

- **Fixed point**: `a706093` (the wave's base commit). Seam-only review, because each ticket was reviewed by its own agent. No review profile exists, so it ran in the orchestrator session.
- **Standards: 8 findings.**
  1. `lesson-format.md` Evidence said `path:line` while step 2 requires permalinks for GitHub sources. Fixed.
  2. The report lacked the coverage note (hard, completion criterion). Fixed: step 6 has a **Coverage** section.
  3. Step 3's subagents did not get step 0's prior lesson names. Fixed: added to their inputs.
  4. Step 6's **Done when** did not check carried-forward lessons (hard). Fixed.
  5. The brief's **Lessons** bullet did not say changed lessons are excluded. Fixed: "the new *match* and *partial* lessons only".
  6. A re-run could file duplicate tickets (hard). Fixed per the user's decision: only lessons adopted in this run get tickets.
  7. `agents/openai.yaml` was unlinked (hard, Reachable files). Fixed per the user's decision: `CODING_STANDARDS.md` exempts harness metadata.
  8. README still said the skill writes only the report. Fixed. README also mentions the thin-target interview.
- **Spec: 4 findings**, all the same seams as Standards 2, 6, 3 and 1, and fixed with them. The reviewer found no conflict between the thin-target interview and a re-run, nor between a GitHub clone and the prior report.
- **Verification**: two headless `claude -p` runs in a row, on `claude-sonnet-5`, effort medium. The first attempt on `claude-opus-5-5` was refused by an API safeguard (`reasoning_extraction`) before doing anything; the user switched the model. The runs used the merged skill via `--plugin-dir`. The source was `https://github.com/mattpocock/skills` and the target a fresh git copy of this repo.
  - **Run 1**: stopped at Lens and Checkpoint. The report has Source (URL, SHA `c55ee46`), Lens, Lessons, "Doesn't transfer, and why" and Coverage, with 16 permalinks all at that SHA. There are exactly 2 tickets for the 2 adopted lessons, in `.scratch/mattpocock-skills/issues/`. The clone was deleted. `git status` listed only the report and the two tickets.
  - **Run 2 (re-run)**: loaded the prior report and stopped at Lens and Checkpoint. No new tickets were filed. The report was updated in place, and every prior decision stood. `git status` listed only ` M docs/lessons/mattpocock-skills.md`. The clone was deleted.
  - **Observation**, not a failure: with source SHA and target unchanged, run 2 reused the prior lessons instead of re-sweeping, and logged this as an ambiguity. Ticket 08's eval may want to state whether that shortcut is allowed.
- **Decisions recorded**: in the comments of tickets 07 (the standards exemption) and 03 (re-run tickets).
- **Traps for the next wave**:
  - Agents in `bypassPermissions` still asked permission for `rm -rf` and `mv` in their own temp directories, and each one needed an orchestrator approval. They are safe to approve when the path is the agent's own temp dir.
  - Agents ended turns while review sub-agents were still running, then continued in autonomous turns that send no notification. Heartbeats caught every one.
  - Two agents hit the session limit mid-turn and were resumed with a narrowed prompt after the reset.
  - Headless smoke runs on `claude-opus-5-5` can be refused by the `reasoning_extraction` safeguard. `claude-sonnet-5` at medium effort ran cleanly.
