"""Theorem D: Sigma(G_1440) <= 215940/899 < 14172/59 <= xi_f(complement of G_1440).

G_1440 = F[(59, 60, 61, 63)] is the clone graph of the 24-vertex magic-square seed F of Section 6.
The two bounds are proved in the text (Section 7).  This script checks, in exact rational
arithmetic, every finite fact the proofs use:

  1. The seed, its exact two-qubit representation (Q_v), and the overlap classes j_v, all taken
     from small_graph_separation.py.  Each context consists of the vertex classes the proof uses:
     row 0 is {4,0,0,0}, rows 1 and 2 are {1,1,1,1}, every column is {2,2,0,0}.
  2. The rank inequality (Lemma 7.3) is tight on the magic-square representation:
     4 tau(Q_0) + 7 + 11 + 9 + 11 + 11 + 9 = 59.  As a classical sanity check, it holds for every
     commuting representation: such a representation is a direct sum of one-dimensional ones, each
     given by a clique of F, and every clique is enumerated.
  3. Lower bound: aggregating the clones of each seed vertex turns the rank inequality into
     d/r >= (83 k_0 + 80 k_1 + 62 k_2 + 11 k_4)/59, which is 14172/59 for G_1440.
  4. Upper bound: for sigma = diag(31, 29, 29, 29)/118 the harmonic weight of each rank-one Q_v is
     1/<psi_v, sigma^{-1} psi_v> = 899/(59(62 - j_v)), and max_v k_v/h_sigma(Q_v) = 215940/899.
     The ancilla dimension K = lcm(59, 60, 61, 63) is divisible by every clone count.
  5. The gap 14172/59 - 215940/899 = 168/53041 is positive.

--perturb lowers the right-hand side of the rank inequality from 59 to 58.  The magic-square
representation must then violate it (exit 1).

Only the standard library is used (numpy enters through small_graph_separation's imports).
Output is deterministic.
"""
import math
import os
import sys
from fractions import Fraction as Fr
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import small_graph_separation as S  # noqa: E402

PROFILE = {0: 59, 1: 60, 2: 61, 4: 63}
COEF_P0 = 4
COEF_CTX = (7, 11, 9, 11, 11, 9)   # rows 0, 1, 2, then columns 0, 1, 2
CENTER = (31, 29, 29, 29)          # sigma = diag(CENTER)/118 in the basis |00>,|01>,|10>,|11>


def fail(what, expected, got):
    print("FAIL: {0}: expected {1}, computed {2}".format(what, expected, got))
    sys.exit(1)


def main():
    rhs = 58 if "--perturb" in sys.argv[1:] else 59

    # 1. seed, representation, classes
    S.check_packing()
    J = S.overlap_classes()
    counts = {j: J.count(j) for j in sorted(set(J))}
    if counts != {0: 9, 1: 8, 2: 6, 4: 1}:
        fail("overlap class sizes", "{0: 9, 1: 8, 2: 6, 4: 1}", counts)
    if J[0] != 4:
        fail("class of vertex 0", 4, J[0])
    ctx_classes = [sorted(J[4 * c + i] for i in range(4)) for c in range(6)]
    want = [[0, 0, 0, 4], [1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 2, 2], [0, 0, 2, 2], [0, 0, 2, 2]]
    if ctx_classes != want:
        fail("classes in each context", want, ctx_classes)
    print("seed: 24 vertices, {0} ordered non-adjacent pairs, exact representation checked".format(
        len(S.FORB)))
    print("overlap classes j = 0, 1, 2, 4 with sizes 9, 8, 6, 1; contexts", ctx_classes)

    # 2. rank inequality: tight on (Q_v); valid on every commuting representation
    tau_q0 = Fr(sum(S.QP[0][i][i][0] for i in range(4)), 4)
    lhs_q = COEF_P0 * tau_q0 + sum(COEF_CTX)
    if lhs_q > rhs:
        fail("rank inequality on the magic-square representation", "<= {0}".format(rhs), lhs_q)
    adj = [[x != y and (x, y) not in S.FORB for y in range(S.N)] for x in range(S.N)]
    cliques = [()]
    for size in range(1, 7):
        for C in combinations(range(S.N), size):
            if all(adj[x][y] for x, y in combinations(C, 2)):
                cliques.append(C)
    worst = max(COEF_P0 * (0 in C) + sum(COEF_CTX[x // 4] for x in C) for C in cliques)
    if worst > rhs:
        fail("rank inequality on commuting representations", "<= {0}".format(rhs), worst)
    largest = max(len(C) for C in cliques)
    print("rank inequality: magic-square representation gives {0} (tight); "
          "{1} cliques (largest {2}) give at most {3}".format(lhs_q, len(cliques), largest, worst))

    # 3. lower bound on xi_f of the complement
    k = [PROFILE[j] for j in J]
    n = sum(k)
    tot = [sum(k[4 * c + i] for i in range(4)) for c in range(6)]
    num = COEF_P0 * k[0] + sum(a * t for a, t in zip(COEF_CTX, tot))
    per_class = {j: 0 for j in PROFILE}
    for v in range(S.N):
        per_class[J[v]] += COEF_P0 * (v == 0) + COEF_CTX[v // 4]
    if per_class != {0: 83, 1: 80, 2: 62, 4: 11}:
        fail("aggregated coefficients per class", "{0: 83, 1: 80, 2: 62, 4: 11}", per_class)
    if num != sum(per_class[j] * PROFILE[j] for j in PROFILE):
        fail("aggregated numerator", num, "other")
    lower = Fr(num, 59)
    print("G = F[(59, 60, 61, 63)]: {0} vertices; context totals {1}".format(n, tot))
    print("lower bound: xi_f(complement) >= (83 k_0 + 80 k_1 + 62 k_2 + 11 k_4)/59 = {0}/59 = {1}".format(
        num, lower))

    # 4. upper bound on Sigma
    tr_c = sum(CENTER)
    h = []
    for v in range(S.N):
        # <psi_v, sigma^{-1} psi_v> = Tr(sigma^{-1} Q_v) for the rank-one projection Q_v
        val = sum(Fr(tr_c, CENTER[i]) * S.QP[v][i][i][0] for i in range(4))
        hv = 1 / val
        if hv != Fr(899, 59 * (62 - J[v])):
            fail("harmonic weight of Q_%d" % v, Fr(899, 59 * (62 - J[v])), hv)
        h.append(hv)
    upper = max(k[v] / h[v] for v in range(S.N))
    tight = sorted(set(J[v] for v in range(S.N) if k[v] / h[v] == upper))
    K = 1
    for j in PROFILE:
        K = K * PROFILE[j] // math.gcd(K, PROFILE[j])
    if any(K % PROFILE[j] for j in PROFILE):
        fail("divisibility of the ancilla dimension", 0, "nonzero remainder")
    print("upper bound: sigma = diag(31,29,29,29)/118, h_sigma(Q_v) = 899/(59(62 - j_v)); "
          "Sigma <= max_v k_v/h_sigma(Q_v) = {0} (attained on classes {1}); K = {2}".format(
              upper, tight, K))

    # 5. the gap
    gap = lower - upper
    if not gap > 0:
        fail("strict separation", "positive gap", gap)
    print("Sigma(G) <= {0} = {1:.6f} < {2:.6f} = {3} <= xi_f(complement of G); gap {4}".format(
        upper, float(upper), float(lower), lower, gap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
