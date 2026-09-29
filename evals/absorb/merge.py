"""Join mechanical.json (check.py) and planted.json (grader agent) into skill-creator's grading.json.

Usage: python evals/absorb/merge.py <run-dir>
"""
import json
import sys
from pathlib import Path

run_dir = Path(sys.argv[1])
expectations = []
for name in ("mechanical.json", "planted.json"):
    path = run_dir / name
    if not path.exists():
        sys.exit(f"{path} is missing: run check.py and the grader before merging")
    expectations += json.loads(path.read_text(encoding="utf-8"))
passed = sum(e["passed"] for e in expectations)
timing = json.loads((run_dir / "timing.json").read_text(encoding="utf-8")) if (run_dir / "timing.json").exists() else {}
grading = {
    "expectations": expectations,
    "summary": {"passed": passed, "failed": len(expectations) - passed, "total": len(expectations),
                "pass_rate": round(passed / len(expectations), 2) if expectations else 0},
    "timing": timing,
}
(run_dir / "grading.json").write_text(json.dumps(grading, indent=2), encoding="utf-8")
print(f"{run_dir}: {passed}/{len(expectations)}")
