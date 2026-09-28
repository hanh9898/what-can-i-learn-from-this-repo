# what-can-i-learn-from-this-repo

`absorb` is an agent skill that distills the lessons worth learning from another repo into the one you're working in.

Point it at a source repo. It reads your project first, sweeps the source, and judges every finding against your project's context. You get a short brief of the lessons that actually fit, you pick the ones to adopt, and it writes a report of every lesson to `docs/lessons/`, including the ones that don't transfer and why.

The method is absorptive capacity (*acquire → assimilate → transform → exploit*). Each lesson is written as a pattern (*context → forces → solution*), and it transfers only when your project shares its forces. Anything else would be cargo cult.

## Install (Claude Code)

```
/plugin marketplace add hanh9898/what-can-i-learn-from-this-repo
/plugin install absorb@absorb
```

## Install (Codex)

Copy the skill folder into your Codex skills location, `~/.agents/skills/` for every project or `.agents/skills/` inside one repo:

```
git clone https://github.com/hanh9898/what-can-i-learn-from-this-repo
mkdir -p ~/.agents/skills
cp -r what-can-i-learn-from-this-repo/skills/absorb ~/.agents/skills/
```

Codex picks the skill up on its own; restart Codex if it doesn't appear. Where Claude Code takes `/absorb <local-path>`, on Codex mention `$absorb` followed by the local path, or just ask.

## Use

From inside the project you want to improve:

```
/absorb <github-url|local-path>
```

Or just ask: "what can I learn from `<repo>`?"

A GitHub URL is shallow-cloned into your OS temp directory for the run and deleted when it ends.

The skill asks you twice: once to correct how it understood your project, and once to pick lessons from the brief. The only file it writes in your project is the report.

## License

MIT
