"""Mechanical assertions [m1]-[m7] of eval 0, checked against one run's outputs.

Usage: python evals/absorb/check.py <run-dir>
Writes <run-dir>/mechanical.json as a list of {text, passed, evidence}, the field names
skill-creator's grading.json and viewer expect. The planted assertions [p*] are graded
by a grader agent, and merge.py joins both into grading.json.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
run_dir = Path(sys.argv[1])
out = run_dir / "outputs"
evals = json.loads((Path(__file__).parent / "evals.json").read_text(encoding="utf-8"))
texts = {e.split("]")[0] + "]": e for e in evals["evals"][0]["expectations"]}


def read(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def section(md, title):
    """Body of the first markdown heading whose text starts with title, up to the next heading of the same level."""
    m = re.search(rf"^(#+)\s*{re.escape(title)}[^\n]*\n", md, re.M | re.I)
    if not m:
        return ""
    level = len(m.group(1))
    rest = md[m.end():]
    end = re.search(rf"^#{{1,{level}}}\s", rest, re.M)
    return rest[: end.start()] if end else rest


reports = sorted((out / "target/docs/lessons").glob("*.md")) if (out / "target/docs/lessons").is_dir() else []
report = read(reports[0]) if reports else ""
tickets = sorted((out / "target/.scratch").rglob("*.md")) if (out / "target/.scratch").is_dir() else []
transcript = read(out / "transcript.md")
results = []


def check(key, passed, evidence):
    results.append({"text": texts[key], "passed": bool(passed), "evidence": evidence})


# m1: report exists and records the source's HEAD SHA.
head = read(out / "source-head.txt").strip()
check("[m1]", reports and head and head in report,
      f"report: {reports[0].name if reports else 'none'}; source HEAD {head or 'unknown'} "
      f"{'found' if head and head in report else 'not found'} in it")

# m2: every lesson in the Lessons section states its forces and its label.
lessons = [b for b in re.split(r"^#{3,4}\s", section(report, "Lessons"), flags=re.M)[1:] if b.strip()]
missing = [b.splitlines()[0][:60] for b in lessons
           if not re.search(r"forces", b, re.I) or not re.search(r"label", b, re.I)]
check("[m2]", lessons and not missing,
      f"{len(lessons)} lessons; missing forces or label: {missing or 'none'}")

# m3: no lesson from "Doesn't transfer" appears in the brief's Lessons part.
dont = section(report, "Doesn't transfer") or section(report, "Doesn’t transfer")
no_names = [n.strip() for n in re.findall(r"^\s*[-*]\s+\*\*(.+?)\*\*", dont, re.M)]
no_names += [n.strip() for n in re.findall(r"^#{3,4}\s+(?:\d+\.\s*)?(.+)$", dont, re.M)]
brief = ""
for block in re.split(r"^## Pause", transcript, flags=re.M)[1:]:
    # The brief is the pause that shows labelled lessons. Its parts are bold labels alone at the
    # start of a line, in the user's language; the first part is Lessons.
    if re.search(r"\*(?:match|partial)\*", block):
        parts = re.split(r"^\*\*(?:[^*\n]|\*(?!\*))+\*\*[^\n]*$", block, flags=re.M)
        brief = parts[1] if len(parts) > 1 else block
leaked = [n for n in no_names if n and n.lower() in brief.lower()]
check("[m3]", brief and no_names and not leaked,
      f"brief found: {bool(brief)}; {len(no_names)} 'doesn't transfer' lessons; in the brief's Lessons part: {leaked or 'none'}")

# m4: only the report and tickets were written.
status = [l for l in read(out / "git-status.txt").splitlines() if l.strip()]
stray = [l for l in status if not re.match(r"^.. (docs/lessons/|\.scratch/)", l)]
check("[m4]", status and not stray, f"{len(status)} changed paths; outside docs/lessons/ and .scratch/: {stray or 'none'}")

# m5: no clone remains in the temp directory.
left = [l for l in read(out / "tmp-after.txt").splitlines() if l.strip()]
check("[m5]", not left, f"temp directory after the run: {left or 'empty'}")

# m6: no fenced block longer than 10 lines in any written file.
long_blocks = []
for f in reports + tickets:
    for block in re.findall(r"^```[^\n]*\n(.*?)^```", read(f), re.M | re.S):
        if block.count("\n") > 10:
            long_blocks.append(f"{f.name}: {block.count(chr(10))} lines")
check("[m6]", not long_blocks, f"fenced blocks over 10 lines: {long_blocks or 'none'}")

# m7: no ticket brings in the source's JS release tooling.
tooling = re.compile(r"\b(?:add|create|introduce|install|set up|adopt)\b[^.\n]{0,60}(?:package\.json|typescript|\bnpm\b|changeset)", re.I)
hits = [f"{t.name}: {tooling.search(read(t)).group(0)}" for t in tickets if tooling.search(read(t))]
check("[m7]", not hits, f"{len(tickets)} tickets; tooling mentions: {hits or 'none'}")

(run_dir / "mechanical.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
for r in results:
    print("PASS" if r["passed"] else "FAIL", r["text"][:60], "|", r["evidence"])
