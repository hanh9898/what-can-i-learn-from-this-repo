# Ticket format

Each adopted lesson becomes one ticket, written so an implementer can pick it up cold.

## Where tickets go

- **Tracker**: when the target has `docs/agents/issue-tracker.md`, file each ticket in the tracker it describes, following its conventions for place, naming and status; the ticket's body takes the fields below. Where it groups tickets by feature, the feature is the source slug. Where the status is a triage state, use its `ready-for-agent` role, since the user adopted the lesson and the ticket is written to be picked up cold.
- **Local**: otherwise, write each ticket as `.scratch/<slug>/NN-<lesson>.md` in the target, where `<lesson>` is the lesson's name lowercased and hyphenated, and `NN` counts up from `01`, after any ticket already in that folder.

## Fields

Title the ticket with the lesson's name, then give it these parts:

- **Work**: what to change in the target: the lesson's solution applied to the target, including the change a *partial* lesson needs. Describe it as a practice, quoting source code only as [`lesson-format.md`](lesson-format.md) allows for a solution.
- **Forces**: the forces the target shares with the source, which say why the work pays off.
- **Acceptance criteria**: a checkbox list, each item a pass/fail check someone can run against the target.
- **Report**: a link to `docs/lessons/<slug>.md`, naming the lesson there. From a file ticket, the link is relative to the ticket's own folder.
- **Source**: the lesson's evidence, pinned to the SHA recorded in step 2 when there is one.

## Carried code

A lesson carries code when its work copies source code into the target instead of rewriting the practice. Its ticket gets one more acceptance criterion: the copied code credits the source and names its licence. The report's **Licence** section records that licence.
