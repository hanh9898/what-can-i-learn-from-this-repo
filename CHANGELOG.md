# Changelog

## 1.0.0 (2026-09-29)

First release of `absorb`, a skill that distils lessons from a source repo into the repo you are in.

- **Sources**: a GitHub URL, shallow-cloned into temp and deleted after the run, or a local path, read in place. Evidence is pinned as permalinks at the source's SHA.
- **Lens**: inferred from the target and confirmed by you. An empty or README-only target gets a short interview instead.
- **Sweep**: one subagent per dimension (architecture, testing, tooling/CI, docs and agent config, conventions, dependencies), or sequential on harnesses without subagents. Large sources get a coverage note.
- **Transform**: every lesson is a pattern (context, forces, solution) labelled *match*, *partial* or *no* against the lens, so cargo cult is named, not adopted.
- **Checkpoint**: a ranked brief of *match* and *partial* lessons, and you pick which to adopt.
- **Exploit**:
  - A report at `docs/lessons/<slug>.md` holds every lesson, your decisions, what doesn't transfer and why, and coverage.
  - Each adopted lesson gets one ticket, in your tracker per `docs/agents/issue-tracker.md`, or else in `.scratch/<slug>/`.
  - A licence note is added when a lesson carries code.
- **Re-runs**: earlier decisions are kept, only new or changed lessons are asked about, and no ticket is filed twice.
- **Install**: a Claude Code plugin marketplace, or copy the skill folder for Codex.

**Evals**:

| Eval | Result |
|---|---|
| Behaviour, with the skill vs no-skill baseline | 11/11 vs 2/11 |
| Trigger, 10 queries including 5 near-misses | 30/30, held-out 12/12 |

Both ran on `claude-sonnet-5`.

**Known gaps**:

- Codex support has not been smoke-tested on a real Codex install.
- The revised behaviour-eval runner has not yet run end to end.
