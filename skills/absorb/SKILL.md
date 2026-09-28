---
name: absorb
description: What can I learn from this repo? Distills the lessons from a source repo (a GitHub URL or a local path) that fit the current repo, and names the ones that don't. Use when the user asks what they can learn from another repo.
argument-hint: "<github-url|local-path>"
---

Transfer what is worth learning from a **source** repo into the **target**, the repo the session stands in. The four phases of absorptive capacity give the order: *acquire* the source, *assimilate* it in its own context, *transform* each finding against the target, *exploit* what the user picks. Every finding is a **lesson**, written as a pattern whose **forces** explain why it works; a lesson transfers only when the target shares its forces. Copying a lesson whose forces the target lacks is **cargo cult**, and the transform phase exists to catch it.

The only file this skill writes in the target is the report. The source is read-only, and the only thing this skill deletes is its own clone of it.

## 1. Lens

Build the target's **lens**: what the target is, its stack and size, the conventions it already holds, and where it hurts. Read its README, agent config (`CLAUDE.md`, `AGENTS.md`), glossary, ADRs, manifest files, directory layout, TODOs and open tickets.

If the target holds no code and none of these files beyond a README (an empty folder, or only a README), it is **thin**: too little to infer from. **Interview** the user about their goals for the target, its planned stack, and where it hurts, then build the lens from their answers and whatever the target holds.

Show the lens to the user in 3–5 lines and ask for corrections.

**Done when** the user accepts the lens.

## 2. Acquire

The source is a GitHub URL or a local path.

- **GitHub URL** (`https://github.com/<owner>/<repo>`): shallow-clone it (`git clone --depth 1`) into a new directory under the OS temp directory, outside the target, and record the clone's exact path. Write every lesson's evidence as a **permalink**, `https://github.com/<owner>/<repo>/blob/<sha>/<path>#L<line>`. When the run ends, at step 6 or at any earlier stop, delete the recorded clone path, and only that path.
- **Local path**: read it in place.

Record the source's full `HEAD` SHA, or "not a git repo".

Name the source's **slug**. A GitHub URL, or a local clone whose `origin` remote is on GitHub (`https://github.com/<owner>/<repo>` or `git@github.com:<owner>/<repo>`, with or without a trailing `.git` or `/`), gives `<owner>-<repo>`. Any other source gives its folder name. Lowercase the slug and turn every run of non-alphanumeric characters into one hyphen. The report lives at `docs/lessons/<slug>.md` in the target.

**Done when** the source is readable, and its slug and SHA (or "not a git repo") are recorded, plus the clone's path for a GitHub URL.

## 3. Assimilate

Map the source's top-level layout and the size of each area. If the source is too large to read in full, as a monorepo usually is, pick the areas the lens points at and skip the rest: the choice is yours, and the user sees it in the brief. Write the **coverage note**: every area read, and every area skipped with the reason the lens gives, or "read in full".

Dispatch one subagent per dimension in [`dimensions.md`](dimensions.md), all at once. Each subagent gets:

- the lens;
- the source's path and SHA, and that the source is read-only;
- its dimension, and whether the lens sends it deep or skims it;
- the areas to read;
- the absolute path of [`lesson-format.md`](lesson-format.md), and the task of writing each finding as a lesson in that format, with the source's context and forces, leaving Label, Payoff and Cost to you.

Without subagents, sweep the dimensions yourself, one after another in the order `dimensions.md` gives, with the same inputs for each.

**Done when** the coverage note is written and every dimension has returned its lessons or "nothing worth transferring".

## 4. Transform

Label every lesson *match*, *partial* or *no* against the lens, each with a one-line reason naming the force the target shares or lacks. Estimate payoff and cost for the *match* and *partial* ones.

**Done when** every lesson carries a label and a reason.

## 5. Checkpoint

Present the **brief**, with these parts in order:

- **Lessons**: the *match* and *partial* lessons only, ranked as [`lesson-format.md`](lesson-format.md) says, each as name, forces, label with reason, payoff, cost, and evidence.
- **Not transferred**: the count of *no* lessons.
- **Coverage**: the coverage note from step 3.
- **Report**: the path the report will be written to.

Ask the user to adopt or reject each lesson.

**Done when** the user has decided on every lesson in the brief.

## 6. Exploit

Write the report to `docs/lessons/<slug>.md`, with these sections in order:

- **Source**: the GitHub URL or local path, the SHA, and the date of the run.
- **Lens**: as the user accepted it.
- **Lessons**: every *match* and *partial* lesson in full format, each with the user's decision.
- **Doesn't transfer, and why**: every *no* lesson, with the missing force.

Tell the user the report's path.

**Done when** the report exists, records a decision for every lesson in the brief, and lists every *no* lesson.
