"""Let skill-creator's run_eval.py read subprocess pipes on Windows.

run_eval polls a subprocess pipe with select(), and Windows select() accepts only sockets, so every
query raised and counted as "not triggered". This select() answers for pipes by polling
PeekNamedPipe until data or EOF arrives or the timeout passes, so run_eval's own timeout still
works, and hands sockets to the real select(). Loaded through PYTHONPATH by run.sh, so the
ProcessPoolExecutor workers get it too; a process that inherits it only ever sees correct select()
semantics.
"""
import os
import select

if os.name == "nt":
    import ctypes
    import msvcrt
    import time
    from ctypes import wintypes

    _real_select = select.select
    _peek = ctypes.windll.kernel32.PeekNamedPipe
    _peek.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p,
                      ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    _peek.restype = wintypes.BOOL

    def _pipe_ready(stream):
        """True when the pipe has bytes to read or has closed; None when it is not a pipe."""
        try:
            handle = msvcrt.get_osfhandle(stream.fileno())
        except (AttributeError, OSError, ValueError):
            return None
        available = wintypes.DWORD()
        if not _peek(handle, None, 0, None, ctypes.byref(available), None):
            return True  # a broken pipe is EOF, which a read reports at once
        return available.value > 0

    def _select(readable, writable, exceptional, timeout=None):
        if writable or exceptional or any(_pipe_ready(r) is None for r in readable):
            return _real_select(readable, writable, exceptional, timeout)
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            ready = [r for r in readable if _pipe_ready(r)]
            if ready or (deadline is not None and time.monotonic() >= deadline):
                return ready, [], []
            time.sleep(0.05)

    select.select = _select
