#!/usr/bin/env bash
# Measure absorb's description against its trigger eval with skill-creator.
# Usage: evals/absorb/trigger/run.sh <results-dir> [loop]
#   default: run_eval, 3 runs per query, writes <results-dir>/results.json
#   loop:    run_loop, the 5-iteration description optimiser. On this Windows machine its runs
#            were killed about 4 s in, before the model replied, so every query read as "not
#            triggered"; trust run_eval's numbers over the loop's.
# Queries run from a throwaway project (a copy of the behaviour-eval fixture), so "this repo"
# means an ordinary skill repo, not the absorb project itself.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"
results="$(mkdir -p "$1" && cd "$1" && pwd)"
mode="${2:-measure}"
skill_creator="${SKILL_CREATOR:-$HOME/.claude/plugins/cache/claude-plugins-official/skill-creator/b819188d2eea/skills/skill-creator}"
model="${ABSORB_EVAL_MODEL:-claude-sonnet-5}"

project="$(mktemp -d "${TMPDIR:-/tmp}/absorb-trigger-XXXX")"
trap 'rm -rf "$project"' EXIT
cp -r "$repo/evals/absorb/fixtures/skill-repo/." "$project/"
mkdir -p "$project/.claude"
git -C "$project" init -q -b main

cd "$project"
# One worker: each run drops its own copy of the skill into the shared .claude/commands, so parallel
# runs of one query show the model several identical skills, and it may pick another run's copy.
# That read as "not triggered" for every query. A cold claude start here also exceeds the 30 s default timeout.
common=(--eval-set "$here/trigger-eval.json" --skill-path "$repo/skills/absorb" --model "$model"
        --num-workers 1 --timeout 120 --runs-per-query 3)
export PYTHONPATH="$here:$skill_creator" PYTHONUTF8=1
if [ "$mode" = loop ]; then
  python -m scripts.run_loop "${common[@]}" --max-iterations 5 --report none --results-dir "$results" --verbose
else
  python -m scripts.run_eval "${common[@]}" > "$results/results.json"
fi
