"""Subprocess entrypoint: run one experiment and print its Result as JSON.

Usage:
    python -m harness.run_experiment experiments.exp_0001_critical_line 300

This is invoked by `harness/verify.py` in a *separate process* so that a
runaway or crashing experiment cannot take down the loop, and so the wall-clock
budget can be enforced with a hard timeout. It prints a single JSON object on
the last line of stdout.
"""
from __future__ import annotations

import importlib
import json
import sys
import time
import traceback

from harness import experiment as exp


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(json.dumps({"status": "ERROR", "error": "usage: run_experiment <module> [budget]"}))
        return 2
    module_name = argv[1]
    budget = float(argv[2]) if len(argv) > 2 else 300.0

    t0 = time.time()
    try:
        mod = importlib.import_module(module_name)
        manifest = getattr(mod, "MANIFEST", None)
        if manifest is not None:
            exp.validate_manifest(manifest)
        if not hasattr(mod, "run"):
            raise exp.ResultError(f"{module_name} defines no run() function")
        res = mod.run(budget)
        res = exp.validate(res)
        elapsed = time.time() - t0
        out = {
            "status": "OK",
            "module": module_name,
            "elapsed_seconds": elapsed,
            "manifest": manifest,
            "result": res,
        }
        # Emit on a single final line so verify.py can parse robustly even if
        # the experiment printed diagnostics to stdout.
        print("__RESULT__" + json.dumps(out))
        return 0
    except exp.ResultError as e:
        print("__RESULT__" + json.dumps({
            "status": "INVALID",
            "module": module_name,
            "elapsed_seconds": time.time() - t0,
            "error": str(e),
        }))
        return 0
    except Exception as e:  # noqa: BLE001 - we want to capture anything
        print("__RESULT__" + json.dumps({
            "status": "FAILED",
            "module": module_name,
            "elapsed_seconds": time.time() - t0,
            "error": f"{type(e).__name__}: {e}",
            "traceback": traceback.format_exc(),
        }))
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
