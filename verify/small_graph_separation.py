"""Exact certificates for QI-120: small clone graphs of the magic-square seed with C_min < log2 Sigma.

For each certified graph G = F[k] (a clone profile k on the 24-vertex magic-square seed F,
constant on the four overlap classes with vertex 0) the script checks, in exact arithmetic:

  1. The seed graph, its exact two-qubit packing, the overlap classes and 48 automorphisms fixing
     vertex 0 that preserve the classes (so the profile is invariant).
  2. A Gibbs witness: a convex combination of complete two-qubit packings with rational states
     sigma = (A^4 |00><00| + B^4 (I-|00><00|))/(A^4+3B^4) and commuting clique packings, giving
     t_W >= t_gibbs, hence 2^C_min(G) <= 1/t_gibbs.
  3. A dual certificate of the harmonic moment relaxation: a rational symmetric matrix Z indexed by
     the 409 monomials, rational mu_x >= 0, every moment equation exact, and Z positive semidefinite
     (a rounded Cholesky factor L with Z - L L^T diagonally dominant, checked in integers).
     This gives t_H <= lam / sum_x mu_x k_x, hence Sigma(G) >= its reciprocal.
  4. t_gibbs > the harmonic bound, i.e. C_min(G) < log2 Sigma(G).

Certificate data: certificates/small_graph_certificates.json.  numpy is used only for a floating
Cholesky proposal and for exact int64 products of bounded integers; every acceptance test is exact.
--perturb adds 1/1000 to one diagonal entry of Z; a moment equation must then fail (exit 1).
--perturb-psd adds 1/2 to a pair of entries of Z at a position whose moment is identically zero, so every
moment equation still holds but Z is no longer positive semidefinite; the exact positivity test must
then fail (exit 1).
"""
import json
import math
import os
import sys
from fractions import Fraction as Fr
from itertools import permutations, product

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def fail(what, expected, got):
    print("FAIL: {0}: expected {1}, computed {2}".format(what, expected, got))
    sys.exit(1)


# ---------------------------------------------------------------- seed graph
BETA = (1, 1, -1)


def cells(c):
    return [(c, j) for j in range(3)] if c < 3 else [(i, c - 3) for i in range(3)]


def parity(c):
    return 1 if c < 3 else BETA[c - 3]


PAT = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
VERT = []
for c in range(6):
    for (s1, s2) in PAT:
        cl = cells(c)
        VERT.append((c, {cl[0]: s1, cl[1]: s2, cl[2]: parity(c) * s1 * s2}))
N = 24
FORB = set()
for x in range(N):
    for y in range(N):
        if x == y:
            continue
        cx, ax = VERT[x]; cy, ay = VERT[y]
        if cx == cy or any(ax[q] != ay[q] for q in set(ax) & set(ay)):
            FORB.add((x, y))


def vid(c, assign):
    cl = cells(c)
    return 4 * c + PAT.index((assign[cl[0]], assign[cl[1]]))


# ---------------------------------------------------------------- exact two-qubit packing
# Gaussian rationals as pairs (re, im) of Fractions; 4x4 matrices as nested lists.
def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def mm(A, B):
    out = []
    for i in range(4):
        row = []
        for j in range(4):
            re = Fr(0); im = Fr(0)
            for k in range(4):
                p = cm(A[i][k], B[k][j]); re += p[0]; im += p[1]
            row.append((re, im))
        out.append(row)
    return out


def kron2(A, B):
    return [[cm(A[i // 2][j // 2], B[i % 2][j % 2]) for j in range(4)] for i in range(4)]


Z0 = (Fr(0), Fr(0)); O1 = (Fr(1), Fr(0))
I2 = [[O1, Z0], [Z0, O1]]
PX = [[Z0, O1], [O1, Z0]]
PZ = [[O1, Z0], [Z0, (Fr(-1), Fr(0))]]
PY = [[Z0, (Fr(0), Fr(-1))], [(Fr(0), Fr(1)), Z0]]
SQ = [[kron2(PZ, I2), kron2(I2, PZ), kron2(PZ, PZ)],
      [kron2(I2, PX), kron2(PX, I2), kron2(PX, PX)],
      [kron2(PZ, PX), kron2(PX, PZ), kron2(PY, PY)]]
ID4 = [[O1 if i == j else Z0 for j in range(4)] for i in range(4)]


def lin(a, A, b, B):
    return [[(a * A[i][j][0] + b * B[i][j][0], a * A[i][j][1] + b * B[i][j][1]) for j in range(4)] for i in range(4)]


QP = []
for x, (c, a) in enumerate(VERT):
    cl = cells(c)
    P = mm(lin(Fr(1, 2), ID4, Fr(a[cl[0]], 2), SQ[cl[0][0]][cl[0][1]]),
           lin(Fr(1, 2), ID4, Fr(a[cl[1]], 2), SQ[cl[1][0]][cl[1][1]]))
    QP.append(P)


def is_zero(A):
    return all(A[i][j] == Z0 for i in range(4) for j in range(4))


def check_packing():
    for x in range(N):
        P = QP[x]
        if mm(P, P) != P:
            fail("projector Q_%d" % x, "Q^2=Q", "no")
        if sum(P[i][i][0] for i in range(4)) != 1:
            fail("rank of Q_%d" % x, 1, "other")
        c, a = VERT[x]
        O3 = SQ[cells(c)[2][0]][cells(c)[2][1]]
        if mm(O3, P) != lin(Fr(a[cells(c)[2]]), P, Fr(0), P):
            fail("third observable eigenvalue", a[cells(c)[2]], "other")
    for (x, y) in FORB:
        if not is_zero(mm(QP[x], QP[y])):
            fail("orthogonality of forbidden pair", (x, y), "nonzero product")
    for c in range(6):
        S = QP[4 * c]
        for x in range(4 * c + 1, 4 * c + 4):
            S = lin(Fr(1), S, Fr(1), QP[x])
        if S != ID4:
            fail("completeness of context %d" % c, "identity", "other")


J = None


def overlap_classes():
    js = [4 * QP[x][0][0][0] for x in range(N)]
    if any(v.denominator != 1 for v in js):
        fail("integral overlap classes", "integers", js)
    return [int(v) for v in js]


# ---------------------------------------------------------------- symmetries fixing vertex 0
def symmetries(Jc):
    etas = [e for e in product((1, -1), repeat=3) if e[0] * e[1] * e[2] == 1]
    out = []
    for pi in [(0, 1, 2), (0, 2, 1)]:
        for kap in permutations(range(3)):
            for eta in etas:
                f = {(0, j): 1 for j in range(3)}
                f.update({(1, j): eta[j] for j in range(3)})
                f.update({(2, j): BETA[j] * BETA[kap[j]] * eta[j] for j in range(3)})
                vmap = [None] * N
                for x, (c, a) in enumerate(VERT):
                    img = {(pi[i], kap[j]): f[(i, j)] * s for (i, j), s in a.items()}
                    c2 = pi[c] if c < 3 else 3 + kap[c - 3]
                    vmap[x] = vid(c2, img)
                if sorted(vmap) != list(range(N)):
                    fail("symmetry is a bijection", "yes", "no")
                if any((vmap[x], vmap[y]) not in FORB for (x, y) in FORB):
                    fail("symmetry is an automorphism", "yes", "no")
                if vmap[0] != 0 or any(Jc[vmap[x]] != Jc[x] for x in range(N)):
                    fail("symmetry fixes vertex 0 and the overlap classes", "yes", "no")
                out.append(tuple(vmap))
    if len(set(out)) != 48:
        fail("number of symmetries", 48, len(set(out)))
    group = set(out)
    for g in out:
        for h in out:
            if tuple(g[h[x]] for x in range(N)) not in group:
                fail("closure of the 48 maps under composition", "a group", "not closed")
    return out


# ---------------------------------------------------------------- moment relaxation words
def redL(w):
    st = []
    for x in w:
        if st and st[-1] == x:
            continue
        if st and (st[-1], x) in FORB:
            return None
        st.append(x)
    return tuple(st)


def redR(w):
    st = []
    for x in w:
        if st and st[-1] == x:
            continue
        st.append(x)
    return tuple(st)


def monomials():
    mons = [((), ())] + [((a,), ()) for a in range(N)] + [((), (b,)) for b in range(N)]
    mons += [((a,), (b,)) for a in range(N) for b in range(N) if a == b or (a, b) not in FORB]
    return mons


def make_canon(syms):
    cache = {}

    def canon(L, R):
        key0 = (L, R)
        if key0 in cache:
            return cache[key0]
        out = None
        L1 = redL(L)
        if L1 is not None:
            R1 = redR(R)
            if R1:
                L1 = redL(L1 + (R1[-1],))           # (P_x (x) E_x) Omega = (I (x) E_x) Omega
                if L1 is not None:
                    L1 = redL((R1[0],) + L1)          # the adjoint relation
            if L1 is not None:
                best = None
                for g in syms:
                    Lg = tuple(g[x] for x in L1); Rg = tuple(g[x] for x in R1)
                    for cand in ((Lg, Rg), (Lg[::-1], Rg[::-1])):
                        if best is None or cand < best:
                            best = cand
                out = best
        cache[key0] = out
        return out
    return canon


def key_table(mons, canon):
    n = len(mons)
    keys = {}
    idx = [[None] * n for _ in range(n)]
    for i, (La, Ra) in enumerate(mons):
        for j in range(i, n):
            Lb, Rb = mons[j]
            k = canon(La[::-1] + Lb, Ra[::-1] + Rb)
            if k is None:
                continue
            if k not in keys:
                keys[k] = len(keys)
            idx[i][j] = idx[j][i] = keys[k]
    return keys, idx


# ---------------------------------------------------------------- Gibbs witness
def cliques_ok(C):
    return all((x, y) not in FORB for x in C for y in C if x != y)


def gibbs_value(prof, Jc, wit):
    parts = []; total = Fr(0)
    for A, B, w in wit["states"]:
        w = Fr(w); total += w
        if not (A > 0 and B > 0 and w >= 0):
            fail("Gibbs witness state", "A, B > 0 and w >= 0", (A, B, w))
        T = A ** 4 + 3 * B ** 4
        parts.append([w * Fr(A ** Jc[x] * B ** (4 - Jc[x]), T) for x in range(N)])
    for C, w in wit["cliques"]:
        w = Fr(w); total += w
        if w < 0:
            fail("clique weight", ">= 0", w)
        if not cliques_ok(C):
            fail("clique", C, "contains a forbidden pair")
        parts.append([w if x in C else Fr(0) for x in range(N)])
    vals = []
    for x in range(N):
        kx = prof[Jc[x]]
        if kx:
            vals.append(sum(p[x] for p in parts) / (kx * total))
    return min(vals)


# ---------------------------------------------------------------- exact positivity
def exact_psd(Zf, gamma):
    """Zf: dict (i,j)->Fraction, symmetric, n x n.  Returns True if Z = L L^T + R with R diagonally
    dominant and nonnegative on the diagonal, all checked in integers."""
    n = NMON
    den = 1
    for v in Zf.values():
        den = den * v.denominator // math.gcd(den, v.denominator)
    Zi = [[0] * n for _ in range(n)]
    for (i, j), v in Zf.items():
        Zi[i][j] = v.numerator * (den // v.denominator)
    Zfl = np.array(Zi, dtype=float) / den
    try:
        Lf = np.linalg.cholesky(Zfl - gamma * np.eye(n))
    except np.linalg.LinAlgError:
        return False
    p = 40
    if np.abs(Lf).max() >= 2.0:
        return False
    Li = np.rint(Lf * 2 ** p).astype(np.int64)
    hi = Li >> 21; lo = Li - (hi << 21)
    HH = hi @ hi.T; HL = hi @ lo.T; LL = lo @ lo.T
    for i in range(n):
        rowsum = 0; diag = None
        for j in range(n):
            prod_ij = (int(HH[i, j]) << 42) + ((int(HL[i, j]) + int(HL[j, i])) << 21) + int(LL[i, j])
            r = (Zi[i][j] << (2 * p)) - den * prod_ij
            if i == j:
                diag = r
            else:
                rowsum += abs(r)
        if diag < rowsum:
            return False
    return True


# ---------------------------------------------------------------- harmonic certificate
def harmonic_bound(prof, Jc, syms, mons, keys, idx, cert, perturb, perturb_psd=False):
    n = len(mons)
    pos = {m: i for i, m in enumerate(mons)}
    Z = {}
    for entry in cert["Z"]:
        i, j, v = entry[0], entry[1], Fr(entry[2])
        for g in syms:
            gi = pos[(tuple(g[x] for x in mons[i][0]), tuple(g[x] for x in mons[i][1]))]
            gj = pos[(tuple(g[x] for x in mons[j][0]), tuple(g[x] for x in mons[j][1]))]
            for (a, b) in ((gi, gj), (gj, gi)):
                if (a, b) in Z and Z[(a, b)] != v:
                    fail("orbit consistency of Z", "single value", (a, b))
                Z[(a, b)] = v
    if perturb:
        Z[(1, 1)] = Z.get((1, 1), Fr(0)) + Fr(1, 1000)
    if perturb_psd:
        a, b = next((i, j) for i in range(n) for j in range(i + 1, n) if idx[i][j] is None)
        for q in ((a, b), (b, a)):
            Z[q] = Z.get(q, Fr(0)) + Fr(1, 2)
    mu = [Fr(v) for v in cert["mu"]]
    if any(m < 0 for m in mu):
        fail("mu nonnegative", ">=0", mu)
    if any(mu[x] != 0 for x in range(N) if prof[Jc[x]] == 0):
        fail("mu vanishes on deleted vertices", 0, mu)
    one = keys[make_canon_cached((), ())]
    S = {}
    for (i, j), v in Z.items():
        k = idx[i][j]
        if k is None:
            continue
        S[k] = S.get(k, Fr(0)) + v
    for x in range(N):
        k = keys[make_canon_cached((), (x,))]
        S[k] = S.get(k, Fr(0)) + mu[x]
    for k, v in S.items():
        if k != one and v != 0:
            fail("moment equation %d" % k, 0, v)
    lam = S.get(one, Fr(0))
    denom = sum(mu[x] * prof[Jc[x]] for x in range(N))
    if denom <= 0:
        fail("normalization", "> 0", denom)
    if not exact_psd(Z, Fr(cert["gamma"]).__float__()):
        fail("exact positive semidefiniteness of Z", "Z = LL^T + diagonally dominant", "not certified")
    return lam, lam / denom, sum(1 for k in S if k != one)


CANON = None
NMON = 0


def make_canon_cached(L, R):
    return CANON(L, R)


def main():
    global J, CANON, NMON
    perturb = "--perturb" in sys.argv[1:]
    perturb_psd = "--perturb-psd" in sys.argv[1:]
    check_packing()
    J = overlap_classes()
    mult = {j: J.count(j) for j in sorted(set(J))}
    print("seed: 24 vertices, %d ordered forbidden pairs; exact two-qubit packing verified" % len(FORB))
    print("overlap classes with vertex 0 (j = 4<00|Q_x|00>):", mult)
    syms = symmetries(J)
    print("48 automorphisms fix vertex 0 and preserve the overlap classes")
    mons = monomials(); NMON = len(mons)
    CANON = make_canon(syms)
    keys, idx = key_table(mons, CANON)
    print("moment relaxation: %d monomials, %d symmetry-reduced moments" % (len(mons), len(keys)))
    data = json.load(open(os.path.join(HERE, "..", "certificates", "small_graph_certificates.json")))
    first = True
    for cert in data["certificates"]:
        prof = {int(a): b for a, b in cert["profile"].items()}
        nv = sum(prof[J[x]] for x in range(N))
        if nv != cert["vertices"]:
            fail("vertex count", cert["vertices"], nv)
        tW = gibbs_value(prof, J, cert["gibbs"])
        if tW != Fr(cert["gibbs"]["t"]):
            fail("Gibbs witness value", cert["gibbs"]["t"], tW)
        lam, tH, neq = harmonic_bound(prof, J, syms, mons, keys, idx, cert["harmonic"], perturb and first,
                                     perturb_psd and first)
        first = False
        if not tW > tH:
            fail("separation t_W > t_H", "strict", (tW, tH))
        gap = (tW - tH) / tH
        print("graph with %d vertices, clone counts per overlap class j=0,1,2,4: %s" % (
            nv, [prof[j] for j in (0, 1, 2, 4)]))
        print("  Gibbs witness:    2^C_min <= 1/t_W = %.6f   (t_W = %s)" % (float(1 / tW), tW))
        print("  harmonic dual:    Sigma  >= 1/t_H = %.6f   (all %d moment equations exact, %d of them"
              " nontrivial; Z >= 0 exact)" % (float(1 / tH), len(keys), neq))
        print("  exact gap: t_W - t_H > 0, relative %.4e; log2 Sigma - C_min >= %.6f bits" % (
            float(gap), float(np.log2(float(tW / tH)))))
    print("QI-120 certificates: all exact checks passed")


if __name__ == "__main__":
    main()
