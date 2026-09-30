"""Context for Theorem C: exact Lovasz and fractional packing numbers of G32, G44, G72.

For each clone graph of certificates/small_graph_certificates.json this script checks, in exact
rational arithmetic, the data in certificates/theorem_c_context.json:

  1. an independent set (pairwise non-adjacent vertices) of the stated size a;
  2. a symmetric rational matrix A with A_xy = 1 whenever x = y or x, y are non-adjacent, given
     orbit-compressed under the 48 seed automorphisms and permutations of clone copies, with
     a*I - A positive semidefinite (exact symmetric elimination).  By Lovasz's dual formula this
     gives theta <= a, and the independent set gives theta >= a, so theta = a;
  3. a fractional packing v >= 0 with sum over every maximal clique <= 1 (all maximal cliques are
     enumerated), and a fractional clique cover w >= 0 with cover >= 1 at every vertex, of equal
     value.  By LP duality that value is alpha*.

It also prints the smallest eigenvalue of each harmonic dual matrix Z, computed in floating point.
These margins only guided the rounding of the certificates; no acceptance test uses them.

--perturb lowers the first claimed bound a to a - 1/1000.  Since theta >= a, the exact positivity
test must then fail (exit 1).

Only numpy and the standard library are used.  Output is deterministic.
"""
import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np

import small_graph_separation as S

HERE = os.path.dirname(os.path.abspath(__file__))


def fail(what, expected, got):
    print("FAIL: {0}: expected {1}, computed {2}".format(what, expected, got))
    sys.exit(1)


def exact_psd(M):
    """Exact test that a symmetric rational matrix is positive semidefinite."""
    M = [row[:] for row in M]
    active = list(range(len(M)))
    while active:
        k = max(active, key=lambda i: M[i][i])
        if M[k][k] < 0:
            return False
        if M[k][k] == 0:
            return all(M[i][j] == 0 for i in active for j in active)
        active.remove(k)
        for i in active:
            f = M[i][k] / M[k][k]
            if f:
                for j in active:
                    M[i][j] -= f * M[k][j]
    return True


def maximal_cliques(adj, n):
    out = []

    def expand(R, P, X):
        if not P and not X:
            out.append(R)
            return
        pivot = max(P | X, key=lambda u: len(adj[u] & P))
        for v in sorted(P - adj[pivot]):
            expand(R + [v], P & adj[v], X & adj[v])
            P = P - {v}
            X = X | {v}
    expand([], set(range(n)), set())
    return out


def main():
    perturb = "--perturb" in sys.argv[1:]
    S.check_packing()
    J = S.overlap_classes()
    syms = S.symmetries(J)
    certs = json.load(open(os.path.join(HERE, "..", "certificates", "small_graph_certificates.json")))
    ctx = json.load(open(os.path.join(HERE, "..", "certificates", "theorem_c_context.json")))
    if len(ctx["graphs"]) != len(certs["certificates"]):
        fail("number of graphs", len(certs["certificates"]), len(ctx["graphs"]))
    mons = S.monomials()
    pos = {m: i for i, m in enumerate(mons)}
    first = True
    for cert, g in zip(certs["certificates"], ctx["graphs"]):
        if g["profile"] != cert["profile"]:
            fail("profile", cert["profile"], g["profile"])
        prof = {int(a): b for a, b in cert["profile"].items()}
        verts = [(x, a) for x in range(S.N) for a in range(prof[J[x]])]
        n = len(verts)
        if n != g["vertices"]:
            fail("vertex count", g["vertices"], n)
        index = {v: i for i, v in enumerate(verts)}

        def adjacent(u, v):
            return u[0] != v[0] and (u[0], v[0]) not in S.FORB
        adj = [set(j for j in range(n) if adjacent(verts[i], verts[j])) for i in range(n)]

        # 1. independent set
        a = g["theta_dual"]["value"]
        ind = [tuple(v) for v in g["independent_set"]]
        if len(set(ind)) != a or any(v not in index for v in ind):
            fail("independent set size", a, len(set(ind)))
        if any(adjacent(u, v) for u in ind for v in ind if u != v):
            fail("independent set", "pairwise non-adjacent", "an adjacent pair")

        # 2. dual matrix for theta
        val = {}
        for x, y, same, q in g["theta_dual"]["entries"]:
            q = Fr(q)
            for s in syms:
                key = (s[x], s[y], same)
                if key in val and val[key] != q:
                    fail("orbit consistency of A", "single value", key)
                val[key] = q
        A = [[None] * n for _ in range(n)]
        for i, (x, ca) in enumerate(verts):
            for j, (y, cb) in enumerate(verts):
                same = x == y and ca == cb
                forced = same or x == y or (x, y) in S.FORB
                if forced:
                    if (x, y, same) in val:
                        fail("forced entry of A", 1, "listed as free")
                    A[i][j] = Fr(1)
                else:
                    if (x, y, same) not in val:
                        fail("free entry of A", "a listed value", (x, y))
                    A[i][j] = val[(x, y, same)]
        if any(A[i][j] != A[j][i] for i in range(n) for j in range(n)):
            fail("symmetry of A", "symmetric", "not symmetric")
        bound = a - Fr(1, 1000) if (perturb and first) else Fr(a)
        M = [[(bound if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]
        if not exact_psd(M):
            fail("exact positive semidefiniteness of a*I - A", "PSD", "not PSD at bound %s" % bound)

        # 3. fractional packing number
        v = [Fr(0)] * n
        for x, c, q in g["packing"]:
            v[index[(x, c)]] = Fr(q)
        if any(t < 0 for t in v):
            fail("packing", ">= 0", "negative entry")
        cliques = maximal_cliques(adj, n)
        worst = max(sum(v[i] for i in C) for C in cliques)
        if worst > 1:
            fail("packing constraint", "<= 1 on every maximal clique", worst)
        cover = [Fr(0)] * n
        total_w = Fr(0)
        for C, w in g["cover"]:
            w = Fr(w)
            C = [index[tuple(u)] for u in C]
            if w < 0:
                fail("cover weight", ">= 0", w)
            if any(j not in adj[i] for i in C for j in C if i != j):
                fail("cover clique", "a clique", C)
            for i in C:
                cover[i] += w
            total_w += w
        if min(cover) < 1:
            fail("clique cover", ">= 1 at every vertex", min(cover))
        if sum(v) != total_w:
            fail("LP duality", "equal primal and dual values", (sum(v), total_w))
        if str(total_w) != g["fractional_packing_number"]:
            fail("stated fractional packing number", g["fractional_packing_number"], total_w)

        # 4. floating-point margin of the harmonic dual matrix Z (information only)
        Z = np.zeros((len(mons), len(mons)))
        for i, j, q in cert["harmonic"]["Z"]:
            q = float(Fr(q))
            for s in syms:
                gi = pos[(tuple(s[x] for x in mons[i][0]), tuple(s[x] for x in mons[i][1]))]
                gj = pos[(tuple(s[x] for x in mons[j][0]), tuple(s[x] for x in mons[j][1]))]
                Z[gi, gj] = Z[gj, gi] = q
        lam = float(np.linalg.eigvalsh(Z).min())
        first = False
        print("graph with %d vertices: independence number %d = Lovasz number (exact); "
              "fractional packing number %s = %.4f (exact LP pair, %d maximal cliques)"
              % (n, a, total_w, float(total_w), len(cliques)))
        print("  smallest eigenvalue of Z (floating point, information only): %.1e" % lam)
    print("Theorem C context: all exact checks passed")


if __name__ == "__main__":
    main()
