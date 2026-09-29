#!/usr/bin/env bash
# Run eval 0 once in one configuration and collect its outputs for skill-creator's grader and viewer.
# Usage: evals/absorb/run.sh <with_skill|without_skill> <run-dir>
# with_skill loads this repo as a plugin; without_skill is the same prompt with no absorb skill.
set -euo pipefail

config="$1"
case "$config" in with_skill|without_skill) ;; *) echo "config must be with_skill or without_skill" >&2; exit 2 ;; esac
run_dir="$(mkdir -p "$2" && cd "$2" && pwd)"
repo="$(cd "$(dirname "$0")/../.." && pwd)"
evals="$repo/evals/absorb/evals.json"
model="${ABSORB_EVAL_MODEL:-claude-sonnet-5}"
effort="${ABSORB_EVAL_EFFORT:-medium}"
field() { python -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); sys.stdout.write(eval(sys.argv[2]))" "$evals" "$1"; }

# The target lives outside this repo, so the run cannot read this repo's CLAUDE.md or tickets.
work="$(mktemp -d "${TMPDIR:-/tmp}/absorb-eval-XXXX")"
trap 'rm -rf "$work"' EXIT
rm -rf "$run_dir/outputs"
mkdir -p "$work/target" "$work/tmp" "$run_dir/outputs"
cp -r "$repo/evals/absorb/fixtures/skill-repo/." "$work/target/"
git -C "$work/target" init -q -b main
git -C "$work/target" add -A
git -C "$work/target" -c user.name=eval -c user.email=eval@example.com commit -qm fixture

prompt="$(field "d['evals'][0]['prompt']")"
plugin_args=()
if [ "$config" = with_skill ]; then plugin_args=(--plugin-dir "$repo"); fi

start=$(date +%s)
(cd "$work/target" && claude -p "${plugin_args[@]}" --permission-mode bypassPermissions \
  --model "$model" --effort "$effort" "$prompt") \
  > "$run_dir/outputs/final-message.md" 2> "$run_dir/stderr.txt" || true
end=$(date +%s)

git -C "$work/target" -c core.quotepath=off status --porcelain -uall > "$run_dir/outputs/git-status.txt"
ls -A "$work/tmp" > "$run_dir/outputs/tmp-after.txt"
for f in transcript.md ambiguities.md; do
  if [ -f "$work/$f" ]; then cp "$work/$f" "$run_dir/outputs/$f"; fi
done
for d in docs/lessons .scratch; do
  if [ -d "$work/target/$d" ]; then mkdir -p "$run_dir/outputs/target/$d" && cp -r "$work/target/$d/." "$run_dir/outputs/target/$d/"; fi
done
git ls-remote "$(field "d['source']['url']")" HEAD | cut -f1 > "$run_dir/outputs/source-head.txt" || true

cat > "$run_dir/timing.json" <<EOF
{"total_duration_seconds": $((end - start)), "model": "$model", "effort": "$effort"}
EOF
