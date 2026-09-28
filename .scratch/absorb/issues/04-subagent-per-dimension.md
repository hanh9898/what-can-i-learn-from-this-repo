# 04: One subagent per dimension, with a coverage note

**What to build:** In the assimilate phase:

- The skill dispatches one subagent per dimension. Each subagent gets the lens and returns lessons in the lesson format. The main agent then does the labelling.
- On a harness without subagents, the skill sweeps the dimensions one after another.
- On a large source, the skill chooses which areas to read based on the lens, and the brief carries a coverage note of what was read and what was skipped.

The wording stays harness-neutral: it names no tool.

**Blocked by:** 01

**Status:** resolved

- [x] On Claude Code, a run dispatches one subagent per dimension, and every dimension returns before labelling starts.
- [x] The skill text names no harness-specific tool and states the sequential fallback.
- [x] On a large source such as a monorepo, the brief includes a coverage note naming the skipped areas, and the user is not asked to scope the run.

## Comments

- **Design**: step 3 first maps the source's layout and area sizes. On a source too large to read in full, the main agent picks areas by the lens on its own and writes a **coverage note** (areas read, areas skipped with the lens's reason, or "read in full"). It then dispatches one subagent per dimension, all at once. Each subagent gets the lens, the source path and SHA with the read-only rule, its dimension and depth, the areas to read, and the absolute path of `lesson-format.md`. It leaves Label, Payoff and Cost to the main agent. The sequential fallback is one sentence: "Without subagents, sweep the dimensions yourself, one after another in the order `dimensions.md` gives, with the same inputs for each." Step 3 is done only when the coverage note is written and every dimension has returned, so labelling (step 4) cannot start earlier. The brief gains a **Coverage** bullet that points at the coverage note. In `dimensions.md`, the order now applies only when one agent sweeps every dimension.
- **Smoke-run setup (2026-09-29)**: to let the runner dispatch its own subagents, each run was a top-level headless Claude Code session (`claude -p --plugin-dir <plugin> --output-format stream-json`), not a subagent. Both checkpoints were pre-answered in the prompt: accept the lens, then adopt the first-ranked lesson and reject the rest. Ambiguities went only to `ambiguities.md`. The large source was a git-initialised snapshot of `claude-plugins-official`: 528 files, 39 plugins plus 14 external plugins, at SHA `d300912`. The target was a git-initialised copy of this repo at `a706093`.
- **Red** (skill at `a706093`, 9.0 min, $2.01): top-level tool calls were Skill 1, Bash 16, Read 1, Write 1, and **Agent 0**. The runner swept every dimension inline. The brief had the parts Lessons, Not transferred and Report, and **no coverage part**. The runner's ambiguity 5 said: "no coverage note, because the current skill does not define one". The transcript had exactly `## Pause 1: 1. Lens` and `## Pause 2: 5. Checkpoint`. Target `git status --porcelain`: only `?? docs/lessons/`. The source was clean.
- **Green** (skill at `7bae56a` without the merge sentence, i.e. the final step 3 text, about 14 min wall time, $6.93):
  - **6 Agent dispatches**, one per dimension, launched back to back.
  - All 6 completion events arrived at stream events 467–591. The main agent wrote "all 6 dimensions have returned; now transform" at event 624 and labelled only after that.
  - Step 3 of the transcript opens with a coverage note: 9 areas read and 4 groups skipped, each with a lens reason (13 LSP plugins, `external_plugins/*`, the security and migration tooling, and 17 hook/MCP/SDK/UI/domain plugins).
  - The brief carries `**Coverage:**` between Not transferred and Report, naming the skipped areas.
  - The transcript has exactly two `## Pause` headings, Lens and Checkpoint, so the user was not asked to scope the run.
  - Target `git status --porcelain`: only `?? docs/lessons/`. The source was clean.
- **Criterion 2** was checked by text, not by a run. A grep of `skills/absorb/*.md` for `Agent|Task|Explore|spawn_agent|general-purpose` finds nothing, and the fallback sentence is quoted above. No harness without subagents was available, so the sequential branch has not been smoke-run.
- **Caveat**: the smoke target is a copy of this repo, so the runner could read this ticket and the spec in `.scratch/`. It cited ticket 04 in its lens. That can bias its area choice, but it does not change what the skill text told it to do.
- **After green**, `dimensions.md` was reworded once more (review finding below). That line only governs the sequential order. Step 3's text is byte-identical to what green ran on.
- **Code review** (fixed point `a706093`, spec this ticket, standard `CODING_STANDARDS.md`):
  - Standards: 1 finding.
    - `dimensions.md` read "sweeps run one after another go in this order". The sentence is broken, and it implies a sequential sweep against step 3's parallel dispatch (Relevance). Fixed: "Each dimension below gets its own sweep. When one agent sweeps them all, it goes in this order."
  - Spec: 2 findings.
    - Scope creep: a sentence added after green told the agent to merge a practice returned by several dimensions into one lesson. Fixed by deleting it. The green run merged duplicates without being told (its ambiguity 4), so the sentence was also a No-op under `CODING_STANDARDS.md`.
    - `dimensions.md` implies a sequential sweep. The same issue as the Standards finding, and fixed.
- **Hand-off to 03** (step 6 is its zone): the spec's report contract lists "the coverage note", but step 6's report sections do not include it. The green runner put it under **Source** (its ambiguity 9). Step 6 should add it, for example as part of **Source** or as its own section pointing at step 3's coverage note.
- **Other runner ambiguities**, left open because they sit outside this ticket's criteria:
  - how many dimensions go deep (`dimensions.md` already gives the rule "where the target hurts or is changing");
  - the payoff scale for ranking (`lesson-format.md`, nobody's zone this wave);
  - the slug `source` for a folder named `source` (ticket 02).
- `claude plugin validate .` passes. This ticket touched no frontmatter or manifest.

