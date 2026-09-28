# 02: Source given as a GitHub URL

**What to build:** Running `/absorb <github-url>` does the following:

- Shallow-clones the source into the OS temp directory, outside the target.
- Records the commit SHA in the report.
- Links every lesson in the brief and the report by a permalink at that SHA.
- Deletes the clone when the run ends.

**Blocked by:** 01

**Status:** resolved

- [x] A run given a GitHub URL completes without the user cloning anything.
- [x] The report states the source URL and the exact SHA that was read.
- [x] Every lesson link is a permalink at that SHA and resolves.
- [x] No clone remains in the temp directory, and nothing except the report was written inside the target.

## Comments

- **Design**:
  - Step 2 Acquire now has two branches. A GitHub URL is shallow-cloned (`git clone --depth 1`) into a new directory under the OS temp directory, and the clone's exact path is recorded. A local path is read in place, as before. Both record the full `HEAD` SHA.
  - The **permalink** form `https://github.com/<owner>/<repo>/blob/<sha>/<path>#L<line>` is defined once, in Acquire, as the shape of every lesson's evidence for a GitHub URL source. Lessons are born with it in step 3, so the brief and the report both carry it without a second rule.
  - The same Acquire bullet deletes the recorded clone path, and only that path, when the run ends (at step 6 or any earlier stop). The intro sentence now says the clone is the only thing the skill deletes.
  - Slug rule (the hand-off from 01): a GitHub URL, or a local clone whose `origin` is on GitHub in https or SSH form, with or without a trailing `.git` or `/`, gives `<owner>-<repo>`; anything else keeps the folder-name rule. Both `https://github.com/mattpocock/skills` and the local clone (origin `git@github.com:mattpocock/skills.git`) give `mattpocock-skills`, checked by a literal-reading subagent.
  - Frontmatter `description` and `argument-hint`, the report's **Source** bullet, and README `## Use` now name GitHub URLs.
- **Deviation from the zone table**: the zone allowed one brief bullet for permalinks. I added one, then removed it after review, because it restated the Acquire rule (single source of truth). The final green run shows the brief carries permalinks without it.
- **Smoke runs** (source `https://github.com/mattpocock/skills`, target a fresh git-initialised copy of this repo at `a706093` minus `.scratch/`; the runner was told the OS temp directory was a `tmp/` folder inside my private temp dir, so every clone stayed there):
  - **Red** (skill at `a706093`): paused at the lens, then halted at Acquire, because the skill only knows local paths and the slug rule needs a folder name. No report, no SHA, no clone. Red on all four criteria.
  - **Green 1** (commit `500302c`): `## Pause 1: Lens`, `## Pause 2: Checkpoint`, nothing else. Report `docs/lessons/mattpocock-skills.md` with the URL and SHA `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`. 4 permalinks, all at that SHA; each file fetched from `raw.githubusercontent.com` at that SHA and each line number within the file. Clone deleted; `git status --porcelain` showed only the report.
  - **Green 2** (final text, after review fixes): same pauses. Report has the URL and the same SHA. The brief and the report each give 4 permalinks at that SHA (some as `#L5-L25` ranges), all resolving by the same check, and neither has a bare `path:line`. The clone `tmp/mattpocock-skills-clone` was deleted and the temp folder is empty. `git status --porcelain --untracked-files=all` shows only `?? docs/lessons/mattpocock-skills.md`.
  - `claude plugin validate .` passed after each frontmatter change.
- **Code review** (fixed point `a706093`):
  - Standards: 3 findings.
    - `lesson-format.md`'s **Evidence** field still says `path:line`, so the evidence shape is split across two files (single source of truth, co-location). Out of zone, so handed off below. The green-2 runner flagged the same conflict but resolved it correctly, taking the more specific Acquire rule.
    - The README line on the temp clone restates the skill's mechanism. Skipped: the README is for human readers, who need to know a clone is made and deleted.
    - The URL branch demanded a 40-character SHA and the local branch did not. Fixed: one shared "Record the source's full `HEAD` SHA" sentence.
  - Spec: 2 findings.
    - Permalinks might not reach the report, and no hand-off was written. Verified instead: both green runs' reports carry permalinks, because lessons are written with them from step 3. The hand-off is below.
    - A literal read of the slug rule might not match an origin ending in `.git`, such as the real local clone's. Fixed: "with or without a trailing `.git` or `/`" now qualifies the match itself.
- **Handed to later tickets / out of zone**:
  - `lesson-format.md` (no owner this wave): the **Evidence** field should read along the lines of "the source location as `path:line`, or as its permalink when step 2 of `SKILL.md` defined one", so the field's definition lives in one place.
  - 03 (step 6): optionally add "and the clone is deleted" to step 6's **Done when**. Not needed to pass this ticket, because both green runs deleted the clone from the Acquire rule alone, but it would make the bound checkable at the step where the run ends.
  - 08 (behaviour eval): the "temp clone removed" assertion can check the path Acquire records.
- **Open**: a run that stops early (for example, the user abandons it at the brief) was not smoke-tested; the Acquire bullet covers it in text only.
