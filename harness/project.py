"""Active-project resolver -- the seam that makes the engine project-agnostic.

The generic engine (experiment contract, verifier, ledger, skeptic, loop) is
problem-independent. Each *project* lives in projects/<name>/ and supplies:
  - a `project.py` module exporting NAME, CONJECTURE, TRACKS,
  - directories: experiments/, prompts/, program.md, lib/, state/, journal/,
    research/.

Select the active project with the INFINILAB_PROJECT env var (a dotted package
name, default "projects.riemann"). Everything else derives from it here, so no
engine module hardcodes a problem.
"""
from __future__ import annotations

import importlib
import os

PKG = os.environ.get("INFINILAB_PROJECT", "projects.riemann")

_pkg_mod = importlib.import_module(PKG)
_cfg = importlib.import_module(PKG + ".project")

NAME = _cfg.NAME
CONJECTURE = getattr(_cfg, "CONJECTURE", NAME)
TRACKS = _cfg.TRACKS

# Filesystem root of the active project (…/projects/<name>).
DIR = os.path.dirname(os.path.abspath(_pkg_mod.__file__))

# Dotted prefix for this project's experiment modules.
EXPERIMENTS_PKG = PKG + ".experiments"


def path(*parts: str) -> str:
    """Absolute path inside the active project directory."""
    return os.path.join(DIR, *parts)
