# 01: Tracer bullet — `absorb` runs end to end on a local source

**What to build:** A user installs this repo as a Claude Code plugin marketplace and runs `/absorb <local-path>` inside a target project. The run then goes:

1. Infer the target **lens** and show it for correction.
2. Sweep every dimension of the source, one after another.
3. Label every **lesson** *match* / *partial* / *no* against the lens.
4. Present a **brief** of the *match* and *partial* lessons, ranked by payoff over cost, and take the user's picks.
5. Write the report described by the spec's report contract: the lens, every lesson with its label and decision, and a "doesn't transfer, and why" section.

The lesson format and the dimension list each live in their own disclosed file, reached by a pointer from the step that needs them. See `.scratch/absorb/spec.md` for the step order and completion criteria.

**Blocked by:** 00

**Status:** resolved

- [x] The repo installs with `/plugin marketplace add`, and `/absorb` appears as a model-invoked skill. The README covers Claude Code install. An MIT licence is present.
- [x] Run from a local clone of `mattpocock/skills` into a small target, the skill stops exactly twice: once at the lens checkpoint and once at the brief.
- [x] Every lesson in the report carries context, forces, solution, a label and a one-line reason. The brief contains no *no* lesson.
- [x] The report records the user's decision for every lesson in the brief, and lists every *no* lesson under "doesn't transfer, and why".
- [x] The run writes only the report in the target, and leaves the local source untouched.
- [x] The skill passes review against `CODING_STANDARDS.md`.

## Comments

- **Smoke run (2026-09-29)**: source was a local clone of `mattpocock/skills` at `2aecca1`, target a temp copy of this repo. The skill stopped twice, at the lens and at the brief. It produced 11 lessons (3 *match*, 4 *partial*, 4 *no*). The brief had 7 lessons and no *no* ones. The report recorded a decision for all 7 and listed the 4 *no* lessons under "Doesn't transfer, and why". `git status` in the target showed only `docs/lessons/`. `claude plugin validate` passed. Its one warning (a root `CLAUDE.md` is not shipped as plugin context) is expected, because that file is repo config.
- **Code review** (fixed point `03ca08e`):
  - Standards: 3 findings.
    - The description did not lead with its trigger. Fixed.
    - The description had two synonymous trigger branches. Fixed: collapsed to one.
    - Possible Duplicated Code: the same description appears in `plugin.json` and `marketplace.json`. Skipped, because each manifest must be self-contained.
  - Spec: 2 findings.
    - The description and `argument-hint` advertised GitHub URLs before ticket 02 exists. Fixed: both are now local-path only.
    - The leading-word ordering. The same issue as Standards finding 1, and fixed.
- **Handed to later tickets**:
  - 02 widens the description and `argument-hint` to GitHub URLs. It also decides the slug so that a local clone and a URL of the same repo map to the same report. The current folder-name rule gave `mattpocock` for `mattpocock/skills`.
  - 06 owns the empty-target interview, which the smoke runner noted as missing.
  - 03 owns tickets.
