# 04: One subagent per dimension, with a coverage note

**What to build:** In the assimilate phase:

- The skill dispatches one subagent per dimension. Each subagent gets the lens and returns lessons in the lesson format. The main agent then does the labelling.
- On a harness without subagents, the skill sweeps the dimensions one after another.
- On a large source, the skill chooses which areas to read based on the lens, and the brief carries a coverage note of what was read and what was skipped.

The wording stays harness-neutral: it names no tool.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] On Claude Code, a run dispatches one subagent per dimension, and every dimension returns before labelling starts.
- [ ] The skill text names no harness-specific tool and states the sequential fallback.
- [ ] On a large source such as a monorepo, the brief includes a coverage note naming the skipped areas, and the user is not asked to scope the run.
