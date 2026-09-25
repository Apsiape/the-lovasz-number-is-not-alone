"""Run every checking script in verify/ and compare its output with the pinned copy.

Usage
-----
    python verify/run_all.py            check; exit 0 only if everything matches
    python verify/run_all.py --bless    re-pin the expected output of every script

What it does
------------
Every ``verify/*.py`` other than this file is run with the current interpreter.
Its complete standard output is compared, byte for byte after normalising line
endings, against ``verify/expected/<name>.txt``. Any of the following makes this
script print a report and exit 1:

* a script exits with a nonzero status (its standard error is shown);
* a script has no pinned expected output;
* a script's output differs from the pinned copy (a unified diff is shown).

Run this before every commit and commit only if it exits 0. Do not re-pin to
make a failure disappear: a check that used to pass and now fails is the most
informative event in this repository, and it gets written up rather than
silenced. Re-pin with ``--bless`` only when the output changed because you meant
it to change, and say in the commit message which value changed and why.
"""

import difflib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED_DIR = os.path.join(HERE, "expected")
REPO = os.path.dirname(HERE)


def normalise(text):
    """Line endings only; nothing else about the output is allowed to vary."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def scripts():
    names = [
        n
        for n in sorted(os.listdir(HERE))
        if n.endswith(".py") and n != os.path.basename(__file__)
    ]
    return names


def run_one(name):
    path = os.path.join(HERE, name)
    proc = subprocess.run(
        [sys.executable, "-u", path],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return proc.returncode, normalise(proc.stdout), normalise(proc.stderr)


def main():
    bless = "--bless" in sys.argv[1:]
    unknown = [a for a in sys.argv[1:] if a != "--bless"]
    if unknown:
        print("run_all: unknown argument(s): {0}".format(" ".join(unknown)))
        print("usage: python verify/run_all.py [--bless]")
        return 1

    if not os.path.isdir(EXPECTED_DIR):
        os.makedirs(EXPECTED_DIR)

    names = scripts()
    if not names:
        print("run_all: no checking scripts found in verify/")
        return 1

    failures = 0
    for name in names:
        stem = name[:-3]
        expected_path = os.path.join(EXPECTED_DIR, stem + ".txt")
        code, out, err = run_one(name)

        if code != 0:
            failures += 1
            print("FAIL {0}: exited with status {1}".format(name, code))
            if out:
                print("--- its output ---")
                sys.stdout.write(out if out.endswith("\n") else out + "\n")
            if err:
                print("--- its error output ---")
                sys.stdout.write(err if err.endswith("\n") else err + "\n")
            print("")
            continue

        if bless:
            with open(expected_path, "w", newline="\n") as handle:
                handle.write(out)
            print("BLESSED {0} -> verify/expected/{1}.txt ({2} lines)".format(
                name, stem, len(out.splitlines())))
            continue

        if not os.path.isfile(expected_path):
            failures += 1
            print("FAIL {0}: no pinned output at verify/expected/{1}.txt".format(name, stem))
            print("     run: python verify/run_all.py --bless")
            print("")
            continue

        with open(expected_path, "r") as handle:
            expected = normalise(handle.read())

        if out != expected:
            failures += 1
            print("FAIL {0}: output differs from verify/expected/{1}.txt".format(name, stem))
            diff = difflib.unified_diff(
                expected.splitlines(True),
                out.splitlines(True),
                fromfile="expected/{0}.txt".format(stem),
                tofile="{0} (this run)".format(name),
            )
            for line in diff:
                sys.stdout.write(line if line.endswith("\n") else line + "\n")
            print("")
            continue

        print("PASS {0}".format(name))

    if bless:
        print("run_all: blessed {0} script(s); now run without --bless".format(len(names)))
        return 0

    print("run_all: {0} script(s), {1} passed, {2} failed".format(
        len(names), len(names) - failures, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
