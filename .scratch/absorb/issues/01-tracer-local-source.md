# 01: Tracer bullet — `absorb` runs end to end on a local source

**What to build:** A user installs this repo as a Claude Code plugin marketplace and runs `/absorb <local-path>` inside a target project. The run then goes:

1. Infer the target **lens** and show it for correction.
2. Sweep every dimension of the source, one after another.
3. Label every **lesson** *match* / *partial* / *no* against the lens.
4. Present a **brief** of the *match* and *partial* lessons, ranked by payoff over cost, and take the user's picks.
5. Write the report described by the spec's report contract: the lens, every lesson with its label and decision, and a "doesn't transfer, and why" section.

The lesson format and the dimension list each live in their own disclosed file, reached by a pointer from the step that needs them. See `.scratch/absorb/spec.md` for the step order and completion criteria.

**Blocked by:** 00

**Status:** ready-for-agent

- [ ] The repo installs with `/plugin marketplace add`, and `/absorb` appears as a model-invoked skill. The README covers Claude Code install. An MIT licence is present.
- [ ] Run from a local clone of `mattpocock/skills` into a small target, the skill stops exactly twice: once at the lens checkpoint and once at the brief.
- [ ] Every lesson in the report carries context, forces, solution, a label and a one-line reason. The brief contains no *no* lesson.
- [ ] The report records the user's decision for every lesson in the brief, and lists every *no* lesson under "doesn't transfer, and why".
- [ ] The run writes only the report in the target, and leaves the local source untouched.
- [ ] The skill passes review against `CODING_STANDARDS.md`.
