"""Numerical upper bounds on theta_alpha(C5) for 0 < alpha < 1/2 plotted in Figure 1.

Each plotted cross is the radius of an explicit witness: the five umbrella vectors u_i in R^3
(<u_i,u_(i+2)> = 0, <u_i,c>^2 = 1/sqrt5) with the faithful center
sigma_x = (1-x)|c><c| + (x/2)(I - |c><c|), where x is optimized at each order by golden-section
search.  By the projection formula, theta_alpha(C5) <= 1 / min_i Z_s(sigma_x, |u_i><u_i|) with
s = 1 - alpha, and Z_s(sigma, |u><u|) = <u|sigma^s|u>^(1/s).

The script rebuilds each witness, evaluates its radius with explicit matrix powers, and checks the
coordinates plotted in paper/main.tex: every plotted value is at least the witness radius (so it is
a valid upper bound) and exceeds it by less than 1e-6 (the plotting precision).  It also checks the
two numbers quoted in the caption.  These are floating-point evaluations of explicit witnesses:
numerical evidence, not exact certificates.

--perturb lowers one plotted value by 1/1000; it then falls below its witness radius and the script
must exit 1.

Only numpy and the standard library are used.  Output is deterministic.
"""
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
C2 = 1 / math.sqrt(5)


def fail(what, expected, got):
    print("FAIL: {0}: expected {1}, computed {2}".format(what, expected, got))
    sys.exit(1)


def umbrella():
    th = math.acos(math.sqrt(C2))
    return [np.array([math.cos(th), math.sin(th) * math.cos(2 * math.pi * i / 5),
                      math.sin(th) * math.sin(2 * math.pi * i / 5)]) for i in range(5)]


def mat_power(sig, s):
    w, V = np.linalg.eigh(sig)
    return (V * w ** s) @ V.T


def radius(alpha, x, U):
    """1 / min_i Z_s(sigma_x, |u_i><u_i|) evaluated with explicit matrices."""
    s = 1 - alpha
    sig = np.diag([1 - x, x / 2, x / 2])
    Ss = mat_power(sig, s)
    return 1 / min(float(u @ Ss @ u) ** (1 / s) for u in U)


def best_x(alpha):
    """Golden-section maximization of q(x) = (1-x)^s c2 + (x/2)^s (1-c2), which is concave."""
    s = 1 - alpha
    q = lambda x: (1 - x) ** s * C2 + (x / 2) ** s * (1 - C2)
    lo, hi = 1e-300, 1 - 1e-12
    g = (math.sqrt(5) - 1) / 2
    for _ in range(300):
        a, b = hi - g * (hi - lo), lo + g * (hi - lo)
        if q(a) < q(b):
            lo = a
        else:
            hi = b
    return (lo + hi) / 2


def plotted():
    tex = open(os.path.join(HERE, "..", "paper", "main.tex")).read()
    m = re.search(r"% numerical upper bounds from explicit witnesses[^\n]*\n\s*\\addplot\[[^\]]*\] coordinates\s*\{([^}]*)\}", tex)
    if not m:
        fail("plotted numerical bounds in paper/main.tex", "an \\addplot block", "none")
    return [(float(a), float(b)) for a, b in re.findall(r"\(([0-9.]+),([0-9.]+)\)", m.group(1))]


def main():
    perturb = "--perturb" in sys.argv[1:]
    U = umbrella()
    for i in range(5):
        if abs(U[i] @ U[(i + 2) % 5]) > 1e-14 or abs(U[i][0] ** 2 - C2) > 1e-14:
            fail("umbrella vectors", "orthogonal pentagon packing", i)
    pts = plotted()
    if perturb:
        pts[3] = (pts[3][0], pts[3][1] - 1e-3)
    print("witness: umbrella vectors with center (1-x)|c><c| + (x/2)(I-|c><c|), x optimized")
    print("  alpha    x*          witness radius   plotted     limiting-handle bound")
    for a, y in pts:
        x = best_x(a)
        r = radius(a, x, U)
        handle = min(2.5, 5 ** (1 / (2 - 2 * a)))
        if not y >= r - 1e-12:
            fail("plotted value at alpha=%g is an upper bound" % a, ">= %.9f" % r, y)
        if not y - r < 1e-6:
            fail("plotted value at alpha=%g matches its witness" % a, "within 1e-6 of %.9f" % r, y)
        if not r < handle:
            fail("witness improves on the displayed bound at alpha=%g" % a, "< %.6f" % handle, r)
        print("  %.3f  %.3e  %.6f       %.6f    %.6f" % (a, x, r, y, handle))
    r1 = radius(0.1, best_x(0.1), U)
    if not (round(r1, 4) == 2.4408 and round(5 ** (1 / 1.8), 4) == 2.4452 and r1 < 5 ** (1 / 1.8)):
        fail("caption values at alpha=0.1", "2.4408 < 2.4452", (r1, 5 ** (1 / 1.8)))
    lo, hi = 0.12, 0.14
    for _ in range(100):
        mid = (lo + hi) / 2
        if radius(mid, best_x(mid), U) < 2.5:
            lo = mid
        else:
            hi = mid
    if round(lo, 3) != 0.128:
        fail("crossing with 5/2", "alpha ~ 0.128", lo)
    print("caption: radius at alpha=0.1 is %.4f < %.4f; below 5/2 until alpha = %.6f" % (
        r1, 5 ** (1 / 1.8), lo))
    print("Pentagon numerical bounds: all checks passed (floating point; evidence only)")


if __name__ == "__main__":
    main()
