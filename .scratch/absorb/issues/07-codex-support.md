# 07: Codex support

**What to build:** A Codex user can copy the skill folder into their skills location and run it. The skill ships Codex metadata alongside it, and the README gains Codex install instructions.

**Blocked by:** 01

**Status:** ready-for-human

- [x] Codex metadata ships inside the skill folder and marks the skill as implicitly invocable.
- [x] The README has a Codex install section.
- [ ] One manual smoke run on Codex fires the skill and completes with the dimensions swept sequentially. The result is recorded in this ticket's comments.

## Comments

- **What changed (2026-09-29)**:
  - `skills/absorb/agents/openai.yaml` is new. It holds `interface.display_name` and `interface.short_description` for the Codex skill picker, plus `policy.allow_implicit_invocation: true`.
  - README has a new `## Install (Codex)` section right after `## Install (Claude Code)`. It copy-installs `skills/absorb` into `~/.agents/skills/` (user level) or `.agents/skills/` (repo level), and maps `/absorb <local-path>` to a `$absorb` mention.
  - The discovery paths and the `openai.yaml` schema come from the official Codex skills docs (`https://learn.chatgpt.com/docs/build-skills`, which `developers.openai.com/codex/skills` redirects to).
- **Discrepancy with the source convention**: mattpocock's `.agents/invocation.md` omits the `policy` block for model-invoked skills and relies on the default `true`. Criterion 1 says the metadata "marks the skill as implicitly invocable", so the file sets the value explicitly. The value still matches `SKILL.md`, which has no `disable-model-invocation`.
- **Red/green check**: a script in the temp dir, run against the worktree. It checks:
  - `agents/openai.yaml` exists and has a display name and a short description.
  - `allow_implicit_invocation` is `true` and `SKILL.md` has no `disable-model-invocation: true`, so the two harnesses agree.
  - README has `## Install (Codex)` directly after `## Install (Claude Code)`.
  - That section names `skills/absorb`, `.agents/skills` and `$absorb`.
  - Red, at `a706093`: exit 1.
    ```
    PASS SKILL.md frontmatter: 'absorb' is model-invoked (no disable-model-invocation: true)
    FAIL skills/absorb/agents/openai.yaml exists inside the skill folder
    FAIL interface.display_name is set
    FAIL interface.short_description is set
    FAIL policy.allow_implicit_invocation is explicitly true
    FAIL Codex policy matches Claude Code invocation (implicit <=> no disable-model-invocation)
    FAIL README has '## Install (Codex)'
    FAIL Codex section copies the skills/absorb folder
    FAIL Codex section names the Codex skills location .agents/skills
    FAIL Codex section shows the Codex invocation $absorb
    9 failure(s)
    ```
  - Green, after the change and again after the review fixes: every check PASS, 0 failures, exit 0. That covers all 11 checks, including the ordering check that the red run could not reach.
  - Install simulation: the README's `mkdir -p` and `cp -r` lines were run with `HOME` set to a temp dir. They produced `~/.agents/skills/absorb/` with `SKILL.md`, `dimensions.md`, `lesson-format.md` and `agents/openai.yaml`.
  - `claude plugin validate .`: passed.
- **Code review** (fixed point `a706093`):
  - Standards: 3 findings.
    - Hard, "Reachable files": nothing links `agents/openai.yaml` from `SKILL.md`. Skipped, for three reasons:
      - The file is harness UI metadata that Codex reads, not reference meant for the agent.
      - Every mattpocock skill ships it unlinked.
      - `SKILL.md` is outside this ticket's zone.
      - Proposed change to `CODING_STANDARDS.md`: exempt harness metadata such as `agents/openai.yaml` from "Reachable files".
    - Judgement, "No-ops": `allow_implicit_invocation: true` restates Codex's default. Skipped, because criterion 1 asks the metadata to mark the skill as implicitly invocable.
    - Judgement, "Wording": "where the next section says `/absorb`" made the reader jump to an unnamed section. Fixed: the sentence now states the mapping directly.
  - Spec: 2 findings.
    - The ticket had no status, ticks or comments yet. Fixed by this update.
    - `$absorb <local-path>` read like documented argument parsing, but Codex documents only the `$skill` mention. Fixed: the README now says to mention `$absorb` followed by the local path. The human run below checks that this works.
- **Open, for a human (criterion 3)**: this machine has no Codex CLI, and Paseo reports the Codex provider unavailable. On a machine with Codex:
  1. Install the skill. This branch is never pushed, so choose the case that applies:
     - **After merge and a push to `main`**: run the README's `## Install (Codex)` commands as written.
     - **Before that**: take a local checkout of the merged `main`, such as the integration checkout `D:\what-can-i-learn-from-this-repo`. Run `mkdir -p ~/.agents/skills`, then `cp -r <checkout>/skills/absorb ~/.agents/skills/`.
  2. Make a throwaway target: `mkdir /tmp/absorb-target && cd /tmp/absorb-target && git init && echo "# demo" > README.md && git add . && git commit -m init`.
  3. Clone a source: `git clone https://github.com/mattpocock/skills /tmp/mp-skills`.
  4. Start `codex` in `/tmp/absorb-target` and ask `what can I learn from /tmp/mp-skills?`. Do not use `$absorb`: this run tests implicit firing.
  5. Check that Codex fires the `absorb` skill. Accept the lens at the first pause and adopt any lesson at the brief.
  6. Check that the dimensions of step 3 are swept one after another, and that the run ends with a report at `docs/lessons/<slug>.md`.
  7. Run `git status --porcelain`. It must list only `docs/lessons/`.
  8. Optional: in a fresh session, run `$absorb /tmp/mp-skills` to confirm the explicit mention in the README.
  9. Record the result here, tick criterion 3, and set the status to `resolved`.
- **Wave 1 review decision (user, 2026-09-29)**: `CODING_STANDARDS.md` "Reachable files" now covers only files an agent reads. Harness metadata the harness reads itself, such as `agents/openai.yaml`, needs no link. This closes the hard Standards finding above.
