# field-notes-skills

Two agent skills I use on my own writing projects. The skill files are the product. There is no build step: the folder is copied into `~/.claude/skills/`.

- `release-checklist`: the checklist I walk through by hand before I publish a new edition of my notes.
- `commit-message`: how the agent should word commit messages in my notes repos.

## Where it hurts

- The agent keeps starting the release checklist on its own when I only mention "release" in passing. Then it asks me checklist questions in the middle of unrelated work.
- `release-checklist/SKILL.md` has grown to a long rules table and a glossary. The agent seems to skim past the steps at the top.
