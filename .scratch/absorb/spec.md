# Spec: `absorb` — distill lessons from a source repo into the current repo

Status: ready-for-agent

## Problem Statement

When I find a repo worth learning from (on GitHub or on disk), turning "this repo is good" into concrete improvements for the project I'm working on is slow and unreliable. Reading someone else's codebase produces a list of things that are impressive in *their* context; half of them don't fit mine, and copying them anyway is cargo cult. The half that do fit are hard to find, hard to justify, and get lost because nothing records why I adopted or rejected them. I want an agent to do this transfer for me, with the rigour of a known framework, and hand me only a short, decision-ready choice.

## Solution

A public, model-invoked skill named `absorb`, invoked as `/absorb <github-url|local-path>` or reached when the user asks something like "what can I learn from this repo". It runs the four phases of **absorptive capacity** (Cohen & Levinthal; Zahra & George): *acquire* the source, *assimilate* it in its own context, *transform* each finding against the target's context, *exploit* the ones the user picks. Every finding is a **lesson** written as a pattern (*context → forces → solution*, after Alexander); a lesson transfers only when the target shares its forces, and the transform phase exists to stop **cargo cult**.

The user is asked twice: once cheaply at the start to correct the target lens, once late to pick lessons from a brief. The run leaves a durable report of every lesson (including the ones that don't transfer, and why) and one ticket per adopted lesson in the target's issue tracker.

## User Stories

1. As a developer, I want to run `/absorb` with a GitHub URL, so that I can learn from a public repo without cloning it myself.
2. As a developer, I want to run `/absorb` with a local path, so that I can learn from a repo already on my disk.
3. As a developer, I want the skill to fire when I ask "what can I learn from this repo" without naming the skill, so that I don't have to remember the command.
4. As a developer, I want the skill to not fire when I only ask to summarise, onboard into, or research a repo, so that it doesn't hijack unrelated requests.
5. As a developer, I want the skill to understand my current project before it reads the source, so that lessons are judged against my context rather than the source's.
6. As a developer, I want to see a 3–5 line summary of how the skill understood my project, so that I can correct a wrong lens before any work builds on it.
7. As a developer with an empty or thin project, I want the skill to interview me about my goals and pain points, so that it still has a lens to judge lessons against.
8. As a developer, I want the skill to sweep a fixed set of dimensions (architecture and module boundaries, testing, tooling/DX/CI, docs and agent config, conventions, dependency choices), so that it finds lessons I didn't know I needed.
9. As a developer, I want my project's lens to decide which dimensions are swept deeply and which are skimmed, so that effort goes where it matters to me.
10. As a developer learning from a very large source repo, I want the skill to choose which areas to read and state what it skipped, so that I'm not asked to scope it and I know the coverage.
11. As a developer, I want each lesson stated as context, forces and solution, so that I can see why it works in the source.
12. As a developer, I want each lesson labelled *match*, *partial* or *no* for whether my project shares its forces, so that I can tell transferable lessons from cargo cult.
13. As a developer, I want the brief to contain only *match* and *partial* lessons, ranked by payoff over cost, so that I can decide quickly.
14. As a developer, I want each lesson in the brief to link to the exact place in the source at the cloned commit, so that I can check it myself and the link never rots.
15. As a developer, I want to pick which lessons to adopt at one checkpoint, so that I'm involved once, late, with everything prepared.
16. As a developer, I want a full report committed in my project recording the source commit, the lens, every lesson, and my decision on each, so that the reasoning survives.
17. As a developer, I want the report to include a "doesn't transfer, and why" section, so that knowing what not to copy is kept as a lesson too.
18. As a developer, I want one ticket per adopted lesson, carrying the work, the forces behind it, checkable acceptance criteria, and links to the report and the source, so that an implementer can pick it up cold.
19. As a developer whose project documents its issue tracker in the shared convention file, I want tickets filed there, so that they land where I track work.
20. As a developer whose project documents no issue tracker, I want tickets written as local markdown files and the brief to say so, so that I'm not asked an extra question.
21. As a developer re-running `/absorb` on the same source, I want my previous decisions kept and only new or changed lessons shown, so that I'm never asked about a lesson I already rejected.
22. As a developer, I want the skill to describe patterns and quote only short snippets, so that my project doesn't absorb someone else's code without a licence check.
23. As a developer adopting a lesson that genuinely needs code carried over, I want the report to state the source's licence and the ticket to require attribution, so that I stay compliant.
24. As a developer, I want the temporary clone removed when the run ends, so that my disk and my project stay clean.
25. As a developer, I want the skill to write only its report and its tickets in my project, so that a learning run never edits my code.
26. As a Codex user, I want the same skill to run on my harness, so that the skill isn't tied to Claude Code.
27. As a user of a harness without subagents, I want the dimensions swept one after another, so that the skill still completes.
28. As a user who has not installed Matt Pocock's skills, I want `absorb` to work standalone, so that I don't need another plugin.
29. As a user who has installed Matt Pocock's skills, I want `absorb` to pick up the shared issue-tracker convention, so that it fits my existing setup.
30. As a user, I want the brief and report in the language I'm speaking, so that I read them comfortably.
31. As a user, I want to install the skill with one plugin-marketplace command, so that installing and updating is trivial.
32. As the skill's author, I want a behavioural eval with a planted gap and a planted cargo-cult trap, so that I can prove the skill beats a no-skill baseline.
33. As the skill's author, I want a small trigger eval including near-misses, so that the description fires when it should and only then.

## Implementation Decisions

- **One skill, `absorb`, model-invoked.** It has a model-facing description carrying the trigger branches ("what can I learn from this repo", learn from / adopt practices of another repo into this one). Written to the repo's coding standards.
- **Harness-neutral wording.** Steps say "one subagent per dimension" without naming a tool; with no subagents, sweep sequentially. Ship Codex metadata alongside the skill.
- **Standalone.** No dependency on other skills. It reads the shared issue-tracker convention file when present, falling back to local markdown tickets under a scratch folder named for the source.
- **Leading words.** *lesson*, *forces*, *cargo cult*, *lens*, *brief*, and the four phase names. The body uses them as tokens and never restates them.
- **Progressive disclosure.** The main skill file holds the ordered steps. The lesson format (pattern fields, force labels, ranking) and the dimension list each live in their own disclosed file, reached by a pointer from the step that needs them.
- **Step order and completion criteria:**
  1. **Prior report.** If a report for this source exists, load its decisions. Done when every prior decision is known.
  2. **Lens.** Infer the target lens from its README, agent config, glossary, ADRs, stack, layout and open issues, then show a 3–5 line summary for correction. If the target is empty or thin, interview instead. Done when the user accepts the lens.
  3. **Acquire.** A URL is shallow-cloned into the OS temp directory, outside the target. A local path is read in place, read-only. Record the commit SHA. Done when the source is readable at a known SHA.
  4. **Assimilate.** One subagent per dimension, each given the lens, each returning lessons in the pattern format. The lens weights depth. For large sources, choose areas by the lens and record what was skipped. Done when every dimension has returned.
  5. **Transform.** The main agent labels every lesson *match*, *partial* or *no* against the lens. Done when every lesson carries a label and a one-line reason.
  6. **Checkpoint.** Present the brief: *match* and *partial* lessons only, ranked by payoff over cost, each with a permalink at the SHA, plus the coverage note and where tickets will go. Prior decisions are not re-asked. Done when the user has decided on every lesson in the brief.
  7. **Exploit.** Write or update the report, then file one ticket per adopted lesson, then delete the temp clone. Done when the report records a decision for every lesson and every adopted lesson has a ticket linking back.
- **Report contract.** One markdown file per source in the target's `docs/lessons/`, named by source slug and committed. It contains the source URL/path and SHA, the lens, the coverage note, every lesson with its label and the user's decision, a "doesn't transfer, and why" section, and licence notes where relevant.
- **Ticket contract.** One ticket per adopted lesson containing the work, the forces (why), checkable acceptance criteria, a link to the report, and a source permalink. No source code beyond short snippets. Attribution is required when code is carried over.
- **Write scope.** The skill writes only the report and the tickets in the target, and deletes only its own temp clone.
- **Output language** follows the user. The skill text is English.
- **Distribution.** The repo is a Claude Code plugin marketplace, installable with `/plugin marketplace add`, MIT licence, with a README covering install for Claude Code and copy-install for Codex.

## Testing Decisions

- **Good tests observe only external behaviour:** the brief shown at the checkpoint, the report file, the tickets, which target files changed, and whether the temp clone is gone. Nothing asserts on internal phases or intermediate reasoning.
- **Seam 1: behaviour.** One end-to-end eval via `skill-creator`, run with the skill and against a no-skill baseline. The source is `mattpocock/skills` pinned at a SHA. The target is a minimal skill-repo fixture with:
  - A planted **gap** that must surface as a *match* lesson: no `disable-model-invocation` where it belongs, and reference not disclosed into separate files.
  - A planted **cargo-cult trap** that must land in "doesn't transfer": the source's TypeScript/npm tooling.

  The lens checkpoint and the lesson choice are pre-answered in the eval prompt, so the run reaches exploit. Mechanical assertions are checked by script:
  - The report exists with the SHA.
  - Every lesson has forces and a label.
  - No *no* lesson appears in the brief.
  - Only the report and tickets were written.
  - The temp clone was removed.
  - No long source-code copies.

  Planted-answer assertions check the gap and the trap. The planted answers are what make the eval discriminate against the baseline.
- **Seam 2: triggering.** Around 10 should/should-not queries via `skill-creator`'s description loop. Near-misses include "summarise this repo", "onboard me into this repo", "review my PR", "compare two libraries" and "research API X". Run only after seam 1 is stable.
- **Manual smoke tests, once each:** empty-target interview branch, re-run preserving decisions, Codex run.
- **Eval location.** Evals and fixtures live at the repo root, outside the distributed skill folder. The `skill-creator` workspace is git-ignored.
- **Prior art:** none in this repo. Follow `skill-creator`'s eval schema and workflow.

## Out of Scope

- Implementing adopted lessons. That is the job of a downstream implementation workflow.
- Splitting a lesson into multiple tickets.
- Copying source files wholesale.
- Scoring or benchmarking repos numerically.
- Learning from non-repo sources (articles, docs sites).
- A non-interactive or CI mode.
- A Codex-specific eval suite.
- Caching clones between runs.
- Multi-source runs in one invocation.

## Further Notes

- `CODING_STANDARDS.md` (the `writing-for-agents` rules plus the `/loop-me` Workflows section) is what review holds this skill to. The two checkpoints follow *push right* and *brief at checkpoints*. The lens checkpoint is a deliberate early exception, because a wrong lens corrupts every later step.
- The repo name `what-can-i-learn-from-this-repo` doubles as the natural trigger phrase.
- The first dogfooding run can be `/absorb` on `mattpocock/skills` into this repo itself.
