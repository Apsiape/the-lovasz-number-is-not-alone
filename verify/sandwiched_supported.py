#!/usr/bin/env python3
"""Finite regressions for Proposition 3.5 (not a proof in arbitrary dimension).

The compressed optimizer is evaluated independently in the ambient definition
of the sandwiched divergence. Tests include noncommuting supports/centers,
rank-one and full supports, mixed and pure competing states, pinching, and
orders 1/2, 1 and infinity. Exact rational checks cover the parameter map and
commuting flat states. Seeded floating-point checks use an explicit tolerance.

Default stdout is pinned by run_all.py. --report writes measured residuals.
--perturb corrupts a minimizing state and must fail the equality check.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import sys
import numpy as np

SEED = 20260929
TOL = 1e-8
ORDERS = (0.5, 0.55, 0.6, 2/3, 0.75, 0.875, 0.95, 0.99, 0.999,
          1.0, 1.001, 1.2, 2.0, 4.0, 8.0, math.inf)
LN2 = math.log(2.0)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def hermitian(a: np.ndarray) -> np.ndarray:
    return (a + a.conj().T) / 2


def positive_function(a: np.ndarray, fn) -> np.ndarray:
    values, vectors = np.linalg.eigh(hermitian(a))
    require(bool(np.min(values) > 0), "A supposedly faithful operator is not positive")
    return hermitian((vectors * fn(values)) @ vectors.conj().T)


def power(a: np.ndarray, exponent: float) -> np.ndarray:
    return positive_function(a, lambda v: np.exp(exponent * np.log(v)))


def unitary(rng: np.random.Generator, d: int) -> np.ndarray:
    a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, _ = np.linalg.qr(a)
    return q


def state(rng: np.random.Generator, d: int, pure: bool = False) -> np.ndarray:
    width = 1 if pure else d
    a = rng.normal(size=(d, width)) + 1j * rng.normal(size=(d, width))
    rho = a @ a.conj().T
    if not pure:
        rho += 0.2 * np.trace(rho).real * np.eye(d) / d
    return hermitian(rho / np.trace(rho).real)


def log_trace_exp(values: np.ndarray) -> float:
    top = float(np.max(values))
    return top + math.log(float(np.exp(values - top).sum()))


def optimizer(sigma: np.ndarray, basis: np.ndarray, beta: float):
    """Compute K_s/Z_s on ran(P), using an orthonormal basis for that range."""
    if beta == 1:
        compressed = hermitian(basis.conj().T @ positive_function(sigma, np.log) @ basis)
        log_k, vec = np.linalg.eigh(compressed)
    else:
        s = -1.0 if math.isinf(beta) else (1.0 - beta) / beta
        compressed = hermitian(basis.conj().T @ power(sigma, s) @ basis)
        vals, vec = np.linalg.eigh(compressed)
        require(bool(np.min(vals) > 0), "Compressed power is not faithful")
        log_k = np.log(vals) / s
    log_z = log_trace_exp(log_k)
    rho = hermitian((vec * np.exp(log_k - log_z)) @ vec.conj().T)
    return rho, -log_z / LN2


def divergence(sigma: np.ndarray, rho: np.ndarray, beta: float, rank: int) -> float:
    """Evaluate the ambient definition; known rank discards numerical zero modes."""
    if beta == 1:
        ev = np.linalg.eigvalsh(hermitian(rho))[-rank:]
        require(bool(np.min(ev) > 0), "Nonzero state eigenvalue was lost")
        return float((np.sum(ev * np.log(ev)) -
                      np.trace(rho @ positive_function(sigma, np.log)).real) / LN2)
    exponent = -0.5 if math.isinf(beta) else (1-beta)/(2*beta)
    left = power(sigma, exponent)
    ev = np.linalg.eigvalsh(hermitian(left @ rho @ left))[-rank:]
    require(bool(np.min(ev) > 0), "Nonzero sandwiched eigenvalue was lost")
    if math.isinf(beta):
        return math.log2(float(ev[-1]))
    return log_trace_exp(beta * np.log(ev)) / ((beta-1) * LN2)


def moment(a: np.ndarray, beta: float, rank: int) -> float:
    vals = np.linalg.eigvalsh(hermitian(a))[-rank:]
    require(bool(np.min(vals) > 0), "Moment lost a nonzero eigenvalue")
    return float(np.sum(vals**beta))


def exact_checks() -> dict[str, int]:
    beta_values = [Fraction(1, 2), Fraction(3, 5), Fraction(2, 3), Fraction(3, 4),
                   Fraction(7, 8), Fraction(1), Fraction(3, 2), Fraction(2),
                   Fraction(4), Fraction(8)]
    for beta in beta_values:
        alpha = 2 - 1/beta
        s = (1-beta)/beta
        require(s + alpha == 1 and 0 <= alpha <= 2, "Exact order map failed")
    sigma = [Fraction(2, 15), Fraction(1, 5), Fraction(2, 3)]
    supports = [(0,), (0, 1), (1, 2), (0, 1, 2)]
    for support in supports:
        mass = sum(sigma[i] for i in support)
        rho = [sigma[i]/mass if i in support else Fraction(0) for i in range(3)]
        require(sum(rho) == 1, "Exact flat-state normalization failed")
        require(all(rho[i]*mass == sigma[i] for i in support),
                "Exact flat-state ratio failed")
    return {"rational_parameter_maps": len(beta_values), "rational_flat_states": len(supports)}


def checks(perturb: bool = False) -> dict:
    report: dict = exact_checks()
    rng = np.random.default_rng(SEED)
    counts = {"supported_cases": 0, "subone_cases": 0, "endpoint_cases": 0,
              "competing_states": 0, "pinching_cases": 0}
    errors = {"max_equality_error_bits": 0.0, "min_competitor_slack_bits": math.inf,
              "max_isometry_error": 0.0, "max_moment_spectrum_error": 0.0,
              "max_pinching_constraint_error": 0.0, "min_pinching_slack": math.inf,
              "min_holder_slack": math.inf}
    perturbed = False
    for d in (2, 3, 5, 8):
        for r in sorted({1, max(1, d//2), d}):
            unit = unitary(rng, d)
            basis = unit[:, :r]
            for kind in ("random", "maximally_mixed", "aligned"):
                if kind == "random":
                    sigma = state(rng, d)
                elif kind == "maximally_mixed":
                    sigma = np.eye(d) / d
                else:
                    vals = np.arange(1, d+1, dtype=float)
                    sigma = hermitian((unit * (vals/vals.sum())) @ unit.conj().T)
                for beta in ORDERS:
                    local, target = optimizer(sigma, basis, beta)
                    require(abs(np.trace(local).real-1) < TOL, "Optimizer trace is not one")
                    require(bool(np.linalg.eigvalsh(local).min() > 0),
                            "Optimizer is not faithful on its prescribed support")
                    if perturb and not perturbed and r > 1 and kind == "random":
                        local = 0.9*local + 0.1*np.eye(r)/r
                        perturbed = True
                    ambient = hermitian(basis @ local @ basis.conj().T)
                    achieved = divergence(sigma, ambient, beta, r)
                    error = abs(achieved-target)
                    errors["max_equality_error_bits"] = max(errors["max_equality_error_bits"], error)
                    require(error <= TOL,
                            f"Supported equality failed (d={d}, r={r}, beta={beta}): {error:.3e} bits")
                    counts["supported_cases"] += 1
                    counts["subone_cases"] += int(beta < 1)
                    counts["endpoint_cases"] += int(beta in (0.5, 1.0, math.inf))
                    for competitor_index in range(20):
                        is_pure = competitor_index % 2 == 0
                        candidate = state(rng, r, pure=is_pure)
                        candidate_rank = 1 if is_pure else r
                        rho = hermitian(basis @ candidate @ basis.conj().T)
                        value = divergence(sigma, rho, beta, candidate_rank)
                        slack = value-target
                        errors["min_competitor_slack_bits"] = min(errors["min_competitor_slack_bits"], slack)
                        require(slack >= -TOL, f"Competing state beats claimed minimum by {-slack:.3e} bits")
                        counts["competing_states"] += 1
                        if beta < 1 and competitor_index == 1:
                            s = (1-beta)/beta
                            a = hermitian(basis.conj().T @ power(sigma, s) @ basis)
                            ahalf = power(a, 0.5)
                            x = hermitian(ahalf @ candidate @ ahalf)
                            v = power(sigma, s/2) @ basis @ power(a, -0.5)
                            iso_error = np.linalg.norm(v.conj().T @ v-np.eye(r), ord=2)
                            left = power(sigma, s/2)
                            equality_error = np.linalg.norm(left @ rho @ left-v @ x @ v.conj().T, ord=2)
                            errors["max_isometry_error"] = max(errors["max_isometry_error"], float(iso_error))
                            errors["max_moment_spectrum_error"] = max(errors["max_moment_spectrum_error"], float(equality_error))
                            require(iso_error <= TOL and equality_error <= TOL,
                                    "Isometric moment reduction failed")
                            av, au = np.linalg.eigh(a)
                            diag = np.real(np.diag(au.conj().T @ x @ au))
                            constraint_error = abs(float(np.sum(diag/av))-1)
                            pinched_moment = float(np.sum(diag**beta))
                            pinching_slack = pinched_moment-moment(x, beta, r)
                            holder_slack = 2**(-(1-beta)*target)-pinched_moment
                            errors["max_pinching_constraint_error"] = max(errors["max_pinching_constraint_error"], constraint_error)
                            errors["min_pinching_slack"] = min(errors["min_pinching_slack"], pinching_slack)
                            errors["min_holder_slack"] = min(errors["min_holder_slack"], holder_slack)
                            require(constraint_error <= TOL, "Pinching changed normalization")
                            require(pinching_slack >= -TOL, "Pinching decreased the sub-one moment")
                            require(holder_slack >= -TOL, "Scalar Holder upper bound failed")
                            counts["pinching_cases"] += 1
    if perturb:
        require(perturbed, "Negative control did not activate")
        raise AssertionError("Corrupted optimizer was not rejected")
    report.update(counts)
    report.update(errors)
    report.update({"seed": SEED, "tolerance": TOL,
                   "orders": ["infinity" if math.isinf(x) else x for x in ORDERS],
                   "scope": "Finite exact/rational and floating-point regressions, not formal verification."})
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--perturb", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = checks(args.perturb)
    except (AssertionError, FloatingPointError, ValueError, np.linalg.LinAlgError) as exc:
        print(f"FAIL sandwiched_supported: {exc}", file=sys.stderr)
        return 1
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS exact rational parameter maps: " + str(report["rational_parameter_maps"]))
    print("PASS exact commuting flat-state identities: " + str(report["rational_flat_states"]))
    print("PASS supported optimizers: " + str(report["supported_cases"]))
    print("PASS sub-one cases: " + str(report["subone_cases"]))
    print("PASS endpoint cases (1/2, 1, infinity): " + str(report["endpoint_cases"]))
    print("PASS competing states: " + str(report["competing_states"]))
    print("PASS isometry, pinching and scalar Holder: " + str(report["pinching_cases"]))
    print("Floating-point tolerance: 1e-8; fixed seed: 20260929")
    print("Scope: finite regressions only; the general proof is Proposition 3.5.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
