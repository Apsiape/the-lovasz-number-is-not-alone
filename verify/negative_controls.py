#!/usr/bin/env python3
"""Run the six corruption tests: the three certificate tests, the optimizer test for the
supported sandwiched minimum, and the tests of the Theorem C context and Figure 1 bound checks.

A nonzero exit alone is insufficient: the expected rejection diagnostic must
also appear, so import errors and missing files are not mistaken for success.
"""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cases = [
        ("entanglement_assisted_spectrum.py", "--perturb", "FAIL: U(alpha_(k+1)) < L(alpha_k)"),
        ("small_graph_separation.py", "--perturb", "FAIL: moment equation"),
        ("small_graph_separation.py", "--perturb-psd", "FAIL: exact positive semidefiniteness of Z"),
        ("sandwiched_supported.py", "--perturb", "Supported equality failed"),
        ("theorem_c_context.py", "--perturb", "FAIL: exact positive semidefiniteness of a*I - A"),
        ("pentagon_numerical_bounds.py", "--perturb", "FAIL: plotted value at alpha="),
    ]
    failures = 0
    for script, flag, marker in cases:
        proc = subprocess.run([sys.executable, str(ROOT / "verify" / script), flag],
                              cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, timeout=180, check=False)
        combined = proc.stdout + proc.stderr
        if proc.returncode != 1 or marker not in combined:
            print(f"FAIL {script} {flag}: expected a targeted rejection", file=sys.stderr)
            print(combined, file=sys.stderr)
            failures += 1
            continue
        print(f"PASS negative control: {script} {flag} rejected")
    print(f"Negative controls: {len(cases)-failures}/{len(cases)} rejected")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
