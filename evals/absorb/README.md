# absorb behaviour eval

One eval, run with the skill and against a no-skill baseline, graded in `skill-creator`'s format. The fixture `fixtures/skill-repo/` plants two things for the source `mattpocock/skills`:

- **A gap** that the skill must adopt as a *match* and ticket: `release-checklist` is run by hand but can be model-invoked, and its reference is inlined.
- **A cargo-cult trap** it must leave under "Doesn't transfer": the source's npm/changesets release tooling. The target has no package manager.

## Run

From the repo root, with `W=evals/absorb-workspace/iteration-<N>/eval-0-mattpocock-skills-into-skill-repo`:

1. `evals/absorb/run.sh with_skill $W/with_skill/run-1` and `evals/absorb/run.sh without_skill $W/without_skill/run-1`. They can run in parallel. Each takes about 5 minutes on `claude-sonnet-5` at medium effort; set `ABSORB_EVAL_MODEL` and `ABSORB_EVAL_EFFORT` to change this. On `claude-opus-5-5`, headless runs have been refused by the `reasoning_extraction` safeguard.
2. `python evals/absorb/check.py <run-dir>` for each run. It writes the mechanical assertions [m1]–[m8] to `mechanical.json`.
3. A grader agent, following `skill-creator`'s `agents/grader.md`, grades [p1]–[p3] into `<run-dir>/planted.json`.
4. `python evals/absorb/merge.py <run-dir>` for each run. It writes `grading.json`.
5. From `skill-creator`'s folder, run `python -m scripts.aggregate_benchmark <abs path to iteration-N> --skill-name absorb`. Then run `PYTHONUTF8=1 python eval-viewer/generate_review.py <iteration-N> --skill-name absorb --benchmark <iteration-N>/benchmark.json --static <iteration-N>/review.html`. On Windows, `PYTHONUTF8=1` is needed because outputs may be in Vietnamese.

`run.sh` puts the target outside this repo, so a run cannot read this repo's `CLAUDE.md` or tickets. The skill always clones the source's current `HEAD`. `evals.json` records the SHA the planted answers were designed against; if the source drifts far from it, recheck the planted answers.
