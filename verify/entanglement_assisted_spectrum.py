"""Controls for Petz graph parameters in the entanglement-assisted spectrum.

What is exact here
------------------
* the integer inequality 2^16 < 5^7 behind the distinctness ladder, and the
  ladder values at 50-digit decimal precision;
* the rational separation L - R, recomputed with fractions.

What is a finite numerical control (it changes no status)
---------------------------------------------------------
* the orthogonal-sum inequality and the compression identity (Lemmas 2 and 3);
* the flagged-mixture inequality (Lemma 5) at orders in [0, 2], and a scope
  witness showing that the same inequality fails at order 3;
* the construction of Proposition 6 on an explicit quantum homomorphism;
* the two pentagon operator bounds (Lemma 8) and the interpolated bound
  (Lemma 9) on random pentagon packings;
* explicit pentagon families giving the upper bounds of Theorem 10, and a
  sigma-optimized umbrella family printed as evidence only.

Deliberate failure: ``--perturb`` replaces the ladder ratio 8 by 7. The claimed
separation U(alpha_1) < L(alpha_0) is then false (5^(1/14) > sqrt5/2) and the
script must exit 1.

Only numpy and the standard library are used. Output is deterministic.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import math
import sys

import numpy as np

TOL = 1e-9          # tolerance for floating-point inequalities (effects are >= 1e-2)
LOG2 = math.log(2.0)


def fail(name, expected, computed):
    print("FAIL: {0}: expected {1}, computed {2}".format(name, expected, computed))
    sys.exit(1)


def require(cond, name, expected, computed):
    if not cond:
        fail(name, expected, computed)


# ---------------------------------------------------------------- linear algebra
def herm(a):
    return (a + a.conj().T) / 2


def fn(a, f, tol=1e-13):
    """Apply f to the eigenvalues above tol; eigenvalues at or below tol map to 0."""
    w, v = np.linalg.eigh(herm(a))
    out = np.array([f(x) if x > tol else 0.0 for x in w])
    return (v * out) @ v.conj().T


def supp(a, tol=1e-11):
    w, v = np.linalg.eigh(herm(a))
    u = v[:, w > tol]
    return u @ u.conj().T


def petz(rho, sig, a):
    """Base-two Petz divergence D_a(rho||sig), a in [0, infinity), with support conventions."""
    if a == 0:
        return -math.log2(np.trace(supp(rho) @ sig).real)
    if a == 1:
        lr = fn(rho, math.log)
        ls = fn(sig, math.log)
        return np.trace(rho @ (lr - ls)).real / LOG2
    q = np.trace(fn(rho, lambda x: x ** a) @ fn(sig, lambda x: x ** (1 - a))).real
    return math.log2(q) / (a - 1)


def comp(P, sig, s):
    """Power-mean compression c_s(P; sig) on the range of the projection P."""
    w, v = np.linalg.eigh(herm(P))
    u = v[:, w > 0.5]
    if s == 0:
        m = u.conj().T @ fn(sig, math.log) @ u
        return float(np.sum(np.exp(np.linalg.eigvalsh(herm(m)))))
    m = u.conj().T @ fn(sig, lambda x: x ** s) @ u
    ev = np.clip(np.linalg.eigvalsh(herm(m)), 1e-300, None)
    return float(np.sum(ev ** (1.0 / s)))


def rand_state(rng, d, rank=None):
    rank = d if rank is None else rank
    x = rng.normal(size=(d, rank)) + 1j * rng.normal(size=(d, rank))
    r = x @ x.conj().T
    return r / np.trace(r).real


def rand_psd(rng, d, rank):
    x = rng.normal(size=(d, rank)) + 1j * rng.normal(size=(d, rank))
    return x @ x.conj().T


def fmt4(x):
    """Four decimals with a sign, printing values below 5e-5 in size as 0.0000."""
    if abs(x) < 5e-5:
        return "0.0000"
    return "{0:+.4f}".format(x)


def schatten(x, p):
    sv = np.linalg.svd(x, compute_uv=False)
    return float(np.sum(sv ** p)) ** (1.0 / p)


# ---------------------------------------------------------------- 1. ladder
def ladder(ratio):
    print("[1] distinctness ladder (exact integers, 50-digit decimals)")
    require(2 ** 16 < 5 ** 7, "2^16 < 5^7", "true", "false")
    print("    2^16 = {0} < 5^7 = {1}".format(2 ** 16, 5 ** 7))
    getcontext().prec = 50
    five = Decimal(5)
    s5 = five.sqrt()

    def lower(r):   # sqrt5 (sqrt5/2)^r, r = alpha/(1-alpha)
        return s5 * ((s5 / 2).ln() * r).exp()

    def upper(r):   # sqrt5 5^(r/2)
        return s5 * ((five.ln() / 2) * r).exp()

    rs = [Decimal(1) / (Decimal(ratio) ** (k + 1)) for k in range(7)]
    for k in range(6):
        a_k = rs[k] / (1 + rs[k])
        lo_k, up_k1 = lower(rs[k]), upper(rs[k + 1])
        print("    k={0} alpha_k={1:.12e}  L(alpha_k)={2:.15f}  U(alpha_k+1)={3:.15f}".format(
            k, float(a_k), float(lo_k), float(up_k1)))
        require(lo_k > s5, "L(alpha_k) > sqrt5", "true", str(lo_k))
        require(up_k1 < lo_k, "U(alpha_(k+1)) < L(alpha_k) at k={0}".format(k),
                "strict", "{0} >= {1}".format(up_k1, lo_k))
    require(upper(rs[0]) < Decimal(5) / 2, "U(alpha_0) < 5/2", "true", str(upper(rs[0])))
    print("    U(alpha_0) = 5^(9/16) = {0:.15f} < 5/2".format(float(upper(rs[0]))))
    print("    all ladder separations strict; values lie in (sqrt5, 5/2)")


# ---------------------------------------------------------------- 2. Rational separation
def qi92():
    print("[2] separation 2^C_min <= R < L <= Sigma (exact fractions)")
    lam = Fraction(11122150566011123, 1853614522304)
    L = Fraction(24001 * 24000 + 24004) / lam
    R = Fraction(24002 ** 4 + 3 * 24001 ** 4, 24002 * 24001 ** 2)
    target = Fraction(538087279416248559183095, 153778236194122166201858782246)
    require(L - R == target, "L-R", str(target), str(L - R))
    require(L - R > 0, "L-R > 0", "positive", str(L - R))
    print("    L - R = {0}/{1} > 0".format((L - R).numerator, (L - R).denominator))
    require(Fraction(5, 2) ** 2 > 5, "(5/2)^2 > 5", "true", "false")
    print("    pentagon: theta(C5)^2 = 5 < 25/4 = (2^C_min(C5))^2")


# ---------------------------------------------------------------- 3. disjoint union lemmas
def disjoint_union(rng):
    print("[3] Lemmas 2-3 (compression identity, orthogonal-sum inequality)")
    worst_sum = 0.0
    worst_id = 0.0
    for trial in range(60):
        d = 6
        sig = rand_state(rng, d)
        q, _ = np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))
        blocks = [q[:, 0:2], q[:, 2:4], q[:, 4:5]]
        projs = [b @ b.conj().T for b in blocks]
        for s in (-1.0, -0.5, 0.0, 0.5, 1.0):
            tot = sum(comp(P, sig, s) for P in projs)
            worst_sum = max(worst_sum, tot)
            require(tot <= 1 + TOL, "orthogonal-sum inequality s={0}".format(s), "<= 1", tot)
        # compression identity on the first block
        b = blocks[0]
        Q = projs[0]
        rho = b @ rand_state(rng, 2) @ b.conj().T
        for a in (0.0, 0.5, 1.0, 1.5, 2.0):
            s = 1 - a
            c = comp(Q, sig, s)
            if s == 0:
                red = b.conj().T @ fn(sig, math.log) @ b
                red = fn(red, math.exp, tol=-1e300)
            else:
                red = b.conj().T @ fn(sig, lambda x: x ** s) @ b
                red = fn(red, lambda x: x ** (1 / s))
            red = red / np.trace(red).real
            lhs = petz(rho, sig, a)
            rhs = petz(b.conj().T @ rho @ b, red, a) - math.log2(c)
            worst_id = max(worst_id, abs(lhs - rhs))
            require(abs(lhs - rhs) < 1e-8, "compression identity a={0}".format(a), rhs, lhs)
    print("    max sum_j c_s(Q_j;sigma) over 60 states, s in {{-1,-1/2,0,1/2,1}}: {0:.4f} <= 1".format(worst_sum))
    print("    compression identity: max deviation below 1e-8: {0}".format(worst_id < 1e-8))


# ---------------------------------------------------------------- 4. flagged mixtures
def flagged(rng):
    print("[4] Lemma 5 (flagged mixture) and its failure above order two")
    orders = (0.0, 0.25, 0.5, 1.0, 1.5, 2.0)
    worst = {a: -1e9 for a in orders}
    viol3 = 0
    maxviol3 = 0.0
    trials = 200
    for trial in range(trials):
        dA = int(rng.integers(2, 4))
        dB = int(rng.integers(2, 4))
        m = int(rng.integers(2, 4))
        parts = [rand_psd(rng, dA, int(rng.integers(1, dA + 1))) for _ in range(m)]
        rho = sum(parts)
        t = np.trace(rho).real
        parts = [x / t for x in parts]
        rho = rho / t
        taus = [rand_state(rng, dB, int(rng.integers(1, dB + 1))) for _ in range(m)]
        sig = rand_state(rng, dB)
        mix = sum(np.kron(x, y) for x, y in zip(parts, taus))
        ref = np.kron(rho, sig)
        for a in orders:
            gap = petz(mix, ref, a) - max(petz(y, sig, a) for y in taus)
            worst[a] = max(worst[a], gap)
            require(gap <= TOL, "flagged mixture at order {0}".format(a), "<= 0", gap)
        gap3 = petz(mix, ref, 3.0) - max(petz(y, sig, 3.0) for y in taus)
        if gap3 > 1e-6:
            viol3 += 1
            maxviol3 = max(maxviol3, gap3)
    for a in orders:
        print("    order {0:.2f}: max [D(mix||rho x sigma) - max_h D(tau_h||sigma)] = {1}".format(a, fmt4(worst[a])))
    require(viol3 > 0 and maxviol3 > 0.5, "order-3 scope witness", "a violation above 0.5 bit", maxviol3)
    print("    order 3.00: the inequality fails in some of the {0} instances, by more than 0.5 bit".format(trials))


# ---------------------------------------------------------------- 5. an explicit quantum homomorphism
def quantum_hom():
    print("[5] Proposition 6 on an explicit quantum homomorphism into K_4")
    signs = [(1, a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
    U = [np.array(s, dtype=complex) / 2 for s in signs]
    n = len(U)
    orth = [[i != j and abs(np.vdot(U[i], U[j])) < 1e-12 for j in range(n)] for i in range(n)]
    Z = np.diag([1, 1j, -1, -1j])
    E = [[np.outer(np.linalg.matrix_power(Z, h) @ u, (np.linalg.matrix_power(Z, h) @ u).conj())
          for h in range(4)] for u in U]
    for i in range(n):
        require(np.allclose(sum(E[i]), np.eye(4)), "sum_h E_u^h = I", "identity", "other")
        for j in range(n):
            if orth[i][j]:
                for h in range(4):
                    require(np.allclose(E[i][h] @ E[j][h], 0), "E_u^h E_v^h = 0", 0, "nonzero")
    # entangled data: block 1 = maximally mixed quantum part (weight 3/10);
    # block 2 = a classical 4-colouring of the orthogonality graph (weight 7/10).
    colour = {}
    for i in range(n):
        used = {colour[j] for j in colour if orth[i][j]}
        colour[i] = min(h for h in range(4) if h not in used)
    w = 0.3
    rho = np.zeros((5, 5), complex)
    rho[:4, :4] = w * np.eye(4) / 4
    rho[4, 4] = 1 - w
    rhs = []
    for i in range(n):
        row = []
        for h in range(4):
            r = np.zeros((5, 5), complex)
            r[:4, :4] = w * E[i][h] / 4
            r[4, 4] = (1 - w) if colour[i] == h else 0
            row.append(r)
        rhs.append(row)
        require(np.allclose(sum(row), rho), "sum_h rho_u^h = rho", "rho", "other")
    for i in range(n):
        for j in range(n):
            if orth[i][j]:
                for h in range(4):
                    require(np.allclose(rhs[i][h] @ rhs[j][h], 0), "Definition 6 orthogonality", 0, "nonzero")
    # target H = four distinguishable letters, tau_h = |h><h|, sigma = I/4, radius exactly 2 bits
    kets = [np.outer(np.eye(4)[h], np.eye(4)[h]).astype(complex) for h in range(4)]
    sig = np.eye(4) / 4
    taup = [sum(np.kron(rhs[i][h], kets[h]) for h in range(4)) for i in range(n)]
    sigp = np.kron(rho, sig)
    for i in range(n):
        for j in range(n):
            if orth[i][j]:
                require(np.allclose(taup[i] @ taup[j], 0), "compatibility of tau'", 0, "nonzero")
    worst = -1e9
    for a in (0.0, 0.5, 1.0, 1.5, 2.0):
        for i in range(n):
            gap = petz(taup[i], sigp, a) - 2.0
            worst = max(worst, gap)
            require(gap <= TOL, "radius of tau' at order {0}".format(a), "<= 2", 2 + gap)
    print("    8 flat vectors in C^4, {0} orthogonal pairs, non-maximally mixed rho".format(
        sum(sum(r) for r in orth) // 2))
    print("    compatibility holds; max_(u,alpha) D_alpha(tau'_u||rho x I/4) - 2 = {0}".format(fmt4(worst)))


# ---------------------------------------------------------------- 6. pentagon operator bounds
def pentagon_packing(rng, d, ranks):
    def sub(r, avoid):
        x = rng.normal(size=(d, r)) + 1j * rng.normal(size=(d, r))
        if avoid is not None:
            qa, _ = np.linalg.qr(avoid)
            x = x - qa @ (qa.conj().T @ x)
        q, _ = np.linalg.qr(x)
        return q
    b0 = sub(ranks[0], None)
    b1 = sub(ranks[1], None)
    b2 = sub(ranks[2], b0)
    b3 = sub(ranks[3], np.hstack([b0, b1]))
    b4 = sub(ranks[4], np.hstack([b1, b2]))
    return [b @ b.conj().T for b in (b0, b1, b2, b3, b4)]


def B(p):
    return 5 ** ((2 - p) / 2) * 2 ** (p - 1)


def pentagon_bounds(rng):
    print("[6] Lemmas 8-9 on random pentagon packings (P_i P_(i+2) = 0)")
    s_list = (1.0, 0.9, 0.75, 0.6, 0.5)
    worst = {s: 0.0 for s in s_list}
    w1 = w2 = 0.0
    count = 0
    while count < 400:
        d = int(rng.integers(3, 7))
        ranks = [int(rng.integers(1, 3)) for _ in range(5)]
        if ranks[0] + ranks[2] > d or ranks[0] + ranks[1] + ranks[3] > d or ranks[1] + ranks[2] + ranks[4] > d:
            continue
        P = pentagon_packing(rng, d, ranks)
        for i in range(5):
            require(np.linalg.norm(P[i] @ P[(i + 2) % 5]) < 1e-9, "pentagon orthogonality", 0, "nonzero")
        X = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        r1 = sum(schatten(Pi @ X @ Pi, 1) for Pi in P) / (math.sqrt(5) * schatten(X, 1))
        r2 = sum(schatten(Pi @ X @ Pi, 2) ** 2 for Pi in P) / (2 * schatten(X, 2) ** 2)
        w1, w2 = max(w1, r1), max(w2, r2)
        require(r1 <= 1 + TOL, "Lemma 8(i)", "<= 1", r1)
        require(r2 <= 1 + TOL, "Lemma 8(ii)", "<= 1", r2)
        sig = rand_state(rng, d)
        sig = fn(sig, lambda x: x ** float(rng.uniform(1, 4)))
        sig = sig / np.trace(sig).real
        for s in s_list:
            r = sum(comp(Pi, sig, s) for Pi in P) / B(1 / s)
            worst[s] = max(worst[s], r)
            require(r <= 1 + TOL, "Lemma 9 at s={0}".format(s), "<= 1", r)
        count += 1
    print("    400 packings in dimensions 3-6, ranks 1-2")
    print("    Lemma 8: max ratios  trace-norm {0:.4f}  Hilbert-Schmidt {1:.4f}  (both <= 1)".format(w1, w2))
    for s in s_list:
        print("    Lemma 9: s={0:.2f} p={1:.4f} B(p)={2:.6f} max sum_i c_s / B(p) = {3:.4f}".format(
            s, 1 / s, B(1 / s), worst[s]))


# ---------------------------------------------------------------- 7. pentagon families
def pentagon_families():
    print("[7] Theorem 10: explicit pentagon families")
    # commuting five-dimensional family, sigma = I/5
    e = np.eye(5)
    rhos = [(np.outer(e[i], e[i]) + np.outer(e[(i + 1) % 5], e[(i + 1) % 5])) / 2 for i in range(5)]
    for i in range(5):
        require(np.allclose(rhos[i] @ rhos[(i + 2) % 5], 0), "commuting family compatibility", 0, "nonzero")
    for a in (0.0, 0.25, 0.5, 1.0, 1.5, 2.0):
        for i in range(5):
            val = petz(rhos[i].astype(complex), np.eye(5) / 5, a)
            require(abs(val - math.log2(2.5)) < 1e-10, "commuting radius order {0}".format(a), math.log2(2.5), val)
    print("    commuting family: D_alpha(rho_i||I/5) = log2(5/2) at alpha in {0,1/4,1/2,1,3/2,2}")
    # umbrella
    c2 = 1 / math.sqrt(5)
    th = math.acos(math.sqrt(c2))
    U = [np.array([math.cos(th), math.sin(th) * math.cos(2 * math.pi * i / 5),
                   math.sin(th) * math.sin(2 * math.pi * i / 5)]) for i in range(5)]
    for i in range(5):
        require(abs(U[i] @ U[(i + 2) % 5]) < 1e-14, "umbrella orthogonality", 0, U[i] @ U[(i + 2) % 5])
        require(abs(U[i][0] ** 2 - c2) < 1e-14, "umbrella handle overlap", c2, U[i][0] ** 2)
    print("    umbrella in R^3: <u_i,u_(i+2)> = 0 and <u_i,c>^2 = 1/sqrt5 verified")
    eps = 1e-9
    for a in (0.0, 0.05, 0.1, 0.2, 0.4):
        sig = np.diag([1 - eps, eps / 2, eps / 2]).astype(complex)
        bound = (1 / (1 - a)) * math.log2(math.sqrt(5)) - math.log2(1 - eps)
        for u in U:
            val = petz(np.outer(u, u).astype(complex), sig, a)
            require(val <= bound + 1e-9, "umbrella radius order {0}".format(a), "<= {0}".format(bound), val)
    print("    umbrella with sigma_eps, eps=1e-9: D_alpha <= log2(sqrt5)/(1-alpha) - log2(1-eps) at 5 orders")
    print("    table: lower bound L, proved upper bound U=min(5/2, 5^(p/2)), and the best value found")
    print("    over umbrella states sigma=diag(1-x,x/2,x/2) (last column is evidence only)")
    grid = np.linspace(0.0005, 0.6, 1200)
    for a in (0.02, 0.05, 0.1, 1 / 9, 0.1217, 0.15, 0.2, 0.3, 0.4, 0.5):
        s = 1 - a
        p = 1 / s
        lo = 5 ** (p / 2) * 2 ** (1 - p)
        up = min(2.5, 5 ** (p / 2))
        best = 0.0
        for x in grid:
            q = (1 - x) ** s * c2 + (x / 2) ** s * (1 - c2)
            best = max(best, 5 * q ** (1 / s))
        num = min(2.5, 5 / best, 5 ** (p / 2))
        require(lo <= num + 1e-12 and lo <= up + 1e-12, "lower bound below explicit upper bounds at alpha={0}".format(a),
                "L <= U", "{0} > {1}".format(lo, min(num, up)))
        print("    alpha={0:.4f}  L={1:.5f}  U={2:.5f}  best-found={3:.5f}".format(a, lo, up, num))
    require(abs(5 ** (2 / 2) * 2 ** (1 - 2) - 2.5) < 1e-15, "L(1/2) = 5/2", 2.5, 5 * 0.5)
    thr = 1 - math.log(5) / (2 * math.log(2.5))
    print("    L(1/2) = 5/2 exactly; pure-handle bound is below 5/2 for alpha < {0:.6f}".format(thr))


def main():
    rng = np.random.default_rng(118)
    ratio = 7 if "--perturb" in sys.argv[1:] else 8
    if ratio != 8:
        print("PERTURBED RUN: ladder ratio 7")
    ladder(ratio)
    qi92()
    disjoint_union(rng)
    flagged(rng)
    quantum_hom()
    pentagon_bounds(rng)
    pentagon_families()
    print("Entanglement-assisted spectrum controls: all checks passed")


if __name__ == "__main__":
    main()
