"""delegation-core v0.6.4 — local MCP delegation server."""

import platform
import sys


# Rich emits Unicode status symbols throughout the CLI. Redirected Windows
# streams otherwise inherit a legacy code page and raise UnicodeEncodeError.
if platform.system() == "Windows":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

# v5.1 patch: this docstring previously read "v0.2.0" while pyproject.toml
# declared 0.5.0 — a stale copy-paste. Kept in lockstep with pyproject going
# forward so `python -c "import delegation_core; print(delegation_core.__doc__)"`
# and `pip show delegation-core` never disagree.
__version__ = "0.6.4"
