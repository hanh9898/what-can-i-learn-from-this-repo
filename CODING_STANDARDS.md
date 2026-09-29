# Coding standards

This repo builds a skill, so the "code" under review is mostly documents an agent consumes: `SKILL.md`, every file it discloses to, `CLAUDE.md`, and `docs/agents/*.md`. The rules below are the reviewer's checklist for those documents, distilled from the `writing-for-agents` skill (the implementing agent loads it while writing; this file is what `/code-review` holds the diff to), plus a Workflows section from `/loop-me`.

For documents, these rules replace the `/code-review` smell baseline; the baseline still applies to any scripts the skill ships. Every rule is a judgement call unless marked **hard**. Each reads _check_ → _fix_.

## Pointers

A pointer is any always-loaded reference to out-of-context material: a skill `description`, a line in `CLAUDE.md`, a link from `SKILL.md` to a disclosed file.

- **Branches listed**: the pointer states what the material is and names each distinct case that should trigger reaching it. → rewrite the pointer until a reader could predict when it fires.
- **Leading word first**: the triggering word opens the pointer. → reorder so it leads.
- **One trigger per branch**: synonyms renaming one branch count as one. → collapse them to the single word we actually use in prompts.
- **Identity cut**: the pointer restates what the body already says. → cut it to what and when.
- **Sharpen before inlining**: must-have material pulled inline because its pointer fired unreliably. → sharpen the pointer's wording first; inline only if that fails.

## Skill mechanics

- **Invocation matches reach**: `disable-model-invocation: true` is set unless the agent must fire the skill on its own or another skill must reach it. → set it, and pay no context load.
- **Description fits its reader**: a user-invoked skill's `description` is a one-line human summary; a model-invoked one carries the trigger branches under the pointer rules above. → rewrite for the right reader.
- **Shared reference placement**: reference needed by two user-invoked skills lives in a plain file outside both. → move it out and point at it from each.
- **Split earns its description**: a new model-invoked skill has its own distinct leading word, or another skill must reach it. → fold it back into its parent.

## Information hierarchy

- **Branch test**: every branch's material sits inline; material only some branches reach sits behind a pointer. → disclose or inline to match.
- **Steps on top**: the ordered steps read without wading through reference that could be disclosed. → push that reference down behind a pointer.
- **Co-location**: a concept's definition, rules, and caveats sit under one heading. → gather the fragments there.
- **Sprawl**: a document long enough that attention thins, even with every line live. → disclose reference, or split by branch or sequence.
- **Reachable files** (**hard**): every file in the skill folder that an agent reads is linked from `SKILL.md` or from a file it links. Harness metadata the harness reads itself, such as `agents/openai.yaml`, needs no link. → add the pointer, or delete the orphan.

## Steps

- **Completion criterion** (**hard**): every step ends on a condition that tells done from not-done. → write the bound.
- **Checkable and exhaustive**: where thoroughness matters, the criterion demands it ("every modified model accounted for", "every rule applied"). → raise the demand in the wording.
- **Sequence splits**: a run of steps is split only when its bound is irreducibly fuzzy and later steps visibly pull the agent to rush; the split crosses a real context boundary (a hand-off or subagent dispatch). → sharpen the bound instead, or move the cut to a real boundary.
- **Split sequences stay split**: a change merging two split sequences exposes each one's later steps. → keep them in separate documents.

## Wording

- **Leading words**: a triad or a sentence gestures at one idea across several sites. → collapse it into one pretrained word, repeated as a token; a coined word is defined once, clearly.
- **Strong enough to steer**: the leading word beats the model's default (_relentless_ over _be thorough_). → pick a stronger word.
- **Positive target**: instructions state the behaviour to do. A prohibition appears only as a hard guardrail with no positive phrasing, and then paired with its positive target. → rewrite as the target behaviour.

## Workflows

Distilled from the `/loop-me` skill. Applies wherever the skill runs a loop (a recurring run) or stops to involve the human, and to any workflow spec under `workflows/`.

- **Trigger named**: each run's trigger is stated as an event (a new email, a new issue) or a schedule, preferring an event where one exists. → name the trigger.
- **Structure earned**: every AI step, checkpoint, and schedule answers a need the spec states. → delete the unearned one.
- **Push right**: each checkpoint sits as late as it will go, so the human is asked once, with all the work done that can be done without them. → move the checkpoint later and do the prep before it.
- **Brief at checkpoints**: a checkpoint shows a decision-ready brief (what was produced, why, a link to the asset). → replace raw output with the brief.
- **Spec done** (**hard**): a workflow spec answers every question an implementer agent would need to ask to build it. → grill the open question into the spec.

## Pruning

- **Single source of truth**: each meaning lives in one place. → keep the authoritative copy, point at it from the rest.
- **Environment over cache**: text restates what one file or one command reveals (`--help`, config, directory layout). → delete it; keep only what looking cannot find: unwritten conventions, reasons, gotchas.
- **Relevance**: every line bears on what the document does, and a change that stales a line removes that line in the same diff. → cut the exposition or the stale layer.
- **No-ops**: a sentence the model already obeys by default. → delete the whole sentence.
