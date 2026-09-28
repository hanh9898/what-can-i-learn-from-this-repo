---
name: absorb
description: What can I learn from this repo? Distills the lessons from a source repo (a local path) that fit the current repo, and names the ones that don't. Use when the user asks what they can learn from another repo.
argument-hint: "<local-path>"
---

Transfer what is worth learning from a **source** repo into the **target**, the repo the session stands in. The four phases of absorptive capacity give the order: *acquire* the source, *assimilate* it in its own context, *transform* each finding against the target, *exploit* what the user picks. Every finding is a **lesson**, written as a pattern whose **forces** explain why it works; a lesson transfers only when the target shares its forces. Copying a lesson whose forces the target lacks is **cargo cult**, and the transform phase exists to catch it.

The only file this skill writes in the target is the report. The source is read-only.

## 1. Lens

Build the target's **lens**: what the target is, its stack and size, the conventions it already holds, and where it hurts. Read its README, agent config (`CLAUDE.md`, `AGENTS.md`), glossary, ADRs, manifest files, directory layout, TODOs and open tickets.

If the target is **thin**, holding no code, manifest or agent config (an empty folder, or only a README), it is too little to infer from. **Interview** the user instead: ask about their goals for the target and their pain points, then build the lens from their answers and whatever the target holds.

Show the lens to the user in 3–5 lines and ask for corrections.

**Done when** the user accepts the lens.

## 2. Acquire

Read a local-path source in place. If it is a git repo, record its `HEAD` SHA.

Name the source's **slug**: its folder name, lowercased, with every run of non-alphanumeric characters turned into one hyphen. The report lives at `docs/lessons/<slug>.md` in the target.

**Done when** the source is readable, and its slug and SHA (or "not a git repo") are recorded.

## 3. Assimilate

Sweep the source one dimension at a time, in the order [`dimensions.md`](dimensions.md) gives, going deep where the lens points and skimming elsewhere. Write each finding as a lesson in the format of [`lesson-format.md`](lesson-format.md), with the source's context and forces, before judging it against the target.

**Done when** every dimension has returned its lessons or "nothing worth transferring".

## 4. Transform

Label every lesson *match*, *partial* or *no* against the lens, each with a one-line reason naming the force the target shares or lacks. Estimate payoff and cost for the *match* and *partial* ones.

**Done when** every lesson carries a label and a reason.

## 5. Checkpoint

Present the **brief**, with these parts in order:

- **Lessons**: the *match* and *partial* lessons only, ranked as [`lesson-format.md`](lesson-format.md) says, each as name, forces, label with reason, payoff, cost, and evidence.
- **Not transferred**: the count of *no* lessons.
- **Report**: the path the report will be written to.

Ask the user to adopt or reject each lesson.

**Done when** the user has decided on every lesson in the brief.

## 6. Exploit

Write the report to `docs/lessons/<slug>.md`, with these sections in order:

- **Source**: path, SHA, and the date of the run.
- **Lens**: as the user accepted it.
- **Lessons**: every *match* and *partial* lesson in full format, each with the user's decision.
- **Doesn't transfer, and why**: every *no* lesson, with the missing force.

Tell the user the report's path.

**Done when** the report exists, records a decision for every lesson in the brief, and lists every *no* lesson.
