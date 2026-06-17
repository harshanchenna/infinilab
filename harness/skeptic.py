"""Tier-2 skeptic: an adversarial reviewer, NOT a truth oracle.

The hard verifier (Tier-1) already proved the experiment *ran* and produced the
numbers it claims. The skeptic does something different and narrower: it reads
the experiment's code + Result and looks for ways the *interpretation* could be
wrong even though the code ran -- numerical artifacts (insufficient precision,
too-coarse grids that miss zeros), overclaiming ("proves RH" vs "consistent
with RH up to T"), misattributed known results, or a frontier metric that is
being gamed rather than genuinely advanced.

Design decisions, grounded in the research on LLM-judge failure modes:
  * The skeptic NEVER decides whether a number is real -- only whether the claim
    around it is sound. Truth stays with the executable spine.
  * It runs as a SEPARATE process/model from the proposer (Opus here), and is
    prompted to falsify, not to praise. This counters self-preference and
    sycophancy bias.
  * Its only power is to DEMOTE: block a result from entering the frontier/KB.
    It cannot promote anything. Worst case it is conservative, never inflating.

Output contract (the model must return a JSON object on its last line):
    {"verdict": "sound" | "overclaimed" | "flawed", "notes": "<= 80 words"}
"""
from __future__ import annotations

import json
import os
import subprocess
from typing import Optional

SKEPTIC_MODEL = os.environ.get("INFINILAB_SKEPTIC_MODEL", "opus")
PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "skeptic.md")


def review(module_path: str, verdict, timeout: int = 600) -> tuple[Optional[str], Optional[str]]:
    """Ask the skeptic model to review a verified result.

    Returns (verdict_str, notes). verdict_str is one of
    {"sound","overclaimed","flawed"} or None if the skeptic could not be run
    (in which case the caller decides a fallback policy).
    """
    try:
        with open(PROMPT_PATH) as f:
            system = f.read()
        with open(_resolve_source(module_path)) as f:
            source = f.read()
    except OSError as e:
        return None, f"skeptic could not read inputs: {e}"

    payload = {
        "experiment_source": source,
        "result": verdict.result,
        "manifest": verdict.manifest,
        "verifier_status": verdict.status,
    }
    user_msg = (
        "Review the following verified experiment. The Tier-1 verifier already "
        "confirmed it ran and produced these numbers; your job is ONLY to judge "
        "whether the claim/interpretation is sound, overclaimed, or flawed.\n\n"
        + json.dumps(payload, indent=2)
        + '\n\nRespond with a single JSON object on the last line: '
        '{"verdict": "sound|overclaimed|flawed", "notes": "..."}'
    )

    try:
        proc = subprocess.run(
            ["claude", "-p", user_msg, "--model", SKEPTIC_MODEL,
             "--append-system-prompt", system],
            capture_output=True, text=True, timeout=timeout,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return None, f"skeptic invocation failed: {e}"

    return _parse(proc.stdout)


def _parse(stdout: str) -> tuple[Optional[str], Optional[str]]:
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            v = obj.get("verdict")
            if v in ("sound", "overclaimed", "flawed"):
                return v, obj.get("notes", "")
        except json.JSONDecodeError:
            continue
    # Couldn't parse a structured verdict; surface raw tail for the ledger.
    return None, (stdout[-400:] if stdout else "no skeptic output")


def _resolve_source(module_path: str) -> str:
    """Map a dotted module path to its source file."""
    rel = module_path.replace(".", os.sep) + ".py"
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), rel)
