"""Experiments: the mutable surface of the lab.

Each module here is one research iteration -- the analog of an edit to
autoresearch's train.py, except we accumulate a library rather than overwrite a
single file, so the whole search history stays in git. Modules must satisfy the
contract in harness/experiment.py (a MANIFEST and a run(budget_seconds) -> Result).
"""
