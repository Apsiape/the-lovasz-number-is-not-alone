#!/usr/bin/env python3
"""Build the complete manuscript without modifying its sources.

Requires pdfLaTeX and BibTeX from a TeX distribution. The bibliography is
regenerated from references.bib. Build products stay in a temporary directory;
the final PDF and the complete console, TeX and BibTeX logs are copied out.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def executable(*names: str) -> str:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError("Required TeX executable not found: " + " or ".join(names))


def build(output: Path, log_dir: Path) -> None:
    pdflatex = executable("pdflatex")
    # Some Debian installations expose the working binary under this name.
    bibtex = executable("bibtex", "bibtex.original", "bibtex8")
    log_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    # Stable timestamps in a fixed TeX environment; not a cross-engine guarantee.
    env.setdefault("SOURCE_DATE_EPOCH", "1790640000")  # 2026-09-29 00:00:00 UTC
    env.setdefault("FORCE_SOURCE_DATE", "1")
    transcripts: list[str] = []
    with tempfile.TemporaryDirectory(prefix="lovasz-build-") as name:
        work = Path(name)
        for source in ("main.tex", "references.bib"):
            shutil.copy2(ROOT / "paper" / source, work / source)
        latex = [pdflatex, "-interaction=nonstopmode", "-halt-on-error",
                 "-file-line-error", "main.tex"]
        steps = [latex, [bibtex, "main"], latex, latex, latex]
        try:
            for index, command in enumerate(steps, start=1):
                print(f"Build step {index}/{len(steps)}: {Path(command[0]).name}", flush=True)
                proc = subprocess.run(command, cwd=work, env=env,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      text=True, encoding="utf-8", errors="replace",
                                      timeout=180, check=False)
                transcripts.append("$ " + " ".join(command) + "\n" + proc.stdout)
                if proc.returncode != 0:
                    raise RuntimeError(f"{Path(command[0]).name} exited {proc.returncode}; "
                                       f"see {log_dir / 'build.log'}")
            final_log = (work / "main.log").read_text(errors="replace")
            for marker in ("There were undefined references", "There were undefined citations",
                           "Label(s) may have changed", "multiply defined"):
                if marker in final_log:
                    raise RuntimeError(f"Unresolved LaTeX diagnostic: {marker}")
            shutil.copy2(work / "main.pdf", output)
        finally:
            (log_dir / "build.log").write_text("\n\n".join(transcripts), encoding="utf-8")
            for suffix in ("log", "blg", "bbl", "aux"):
                source = work / ("main." + suffix)
                if source.exists():
                    shutil.copy2(source, log_dir / source.name)
    print(f"Built: {output}")
    print(f"Logs:  {log_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "output/pdf/the-lovasz-number-is-not-alone-v1.1.pdf")
    parser.add_argument("--log-dir", type=Path, default=ROOT / "output/build")
    args = parser.parse_args()
    try:
        build(args.output.resolve(), args.log_dir.resolve())
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
