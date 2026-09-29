"""Let skill-creator's run_eval.py work on Windows, where select() only accepts sockets.

On Windows its select() on a subprocess pipe raises. Reporting the pipe as always ready
turns the loop into blocking reads, and it still checks its timeout between stream events.
Loaded through PYTHONPATH by run.sh, so the ProcessPoolExecutor workers get it too.
"""
import os
import select

if os.name == "nt":
    select.select = lambda readable, writable, exceptional, timeout=None: (list(readable), [], [])
