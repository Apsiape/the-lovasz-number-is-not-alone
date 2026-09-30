# Changelog

## 1.1.0 — 30 September 2026

Theorems A–C, every certificate value and the numbering of version 1.0.0 are
unchanged; the one new lemma is placed last (Lemma B.2).

### Mathematics

- **Proposition 3.5** now proves
  `sandwiched_theta_beta(G) = theta_{2-1/beta}(G)` for the whole range
  `1/2 <= beta <= infinity` (version 1.0.0: `beta >= 1`). The sub-one argument
  uses an isometric reduction to a compressed moment, pinching and scalar
  Hölder, and gives an explicit minimizer faithful on the prescribed support.
  The endpoints `1/2`, `1` and `infinity` are treated directly, and no limit is
  exchanged with an unbounded-dimension infimum. Frank–Lieb (2013) is cited
  for data processing of the sandwiched family.
- **Correction.** Figure 4 and Section 7 of version 1.0.0 stated that both
  illustrated pentagon geometries are nonoptimal throughout `0 < alpha < 1/2`;
  the displayed bounds do not establish this. Version 1.1.0 states the proved
  regimes (the flat witness is optimal on `[1/2, 2]`; the umbrella attains the
  order-zero value) and leaves the intermediate graph value open. The captions
  of Figures 1 and 4 distinguish the limiting handle-center witness from an
  optimized center, and the crossing of two upper bounds from a transition in
  the graph value.

### Exposition

- Section 5.4 quotes Duan and Winter's definitions of `Sigma(G)` and
  `S_0,NS(G)`, their Lemma 23, the remark after their chain and their pentagon
  conjecture (from arXiv:1409.3426v3, which numbers the chain (53) instead of
  the journal's (54)), and explains why their Proposition 18 does not give the
  graph-level single-letter formula.
- Appendix B.4 (Lemma B.2) derives equations (9)–(10) from Li and Zuiddam's
  Definition 6 and their complement convention.
- Figure 1 adds numerical upper bounds on `theta_alpha(C5)` for
  `0.04 <= alpha <= 0.125` from explicit witnesses (umbrella vectors with an
  optimized faithful center): 2.4408 < 2.4452 at `alpha = 0.1`, below 5/2 until
  `alpha` is about 0.128. The shaded band and all curves are unchanged.
- Theorem C is followed by `theta = 6, 8, 12` and `alpha* = 32/5, 37/4, 72/5`
  for G32, G44, G72, and the smallest eigenvalues of the dual matrices.
- Every cross-reference carries an explicit type, so references print with the
  correct name under any TeX distribution.

### Package

- New checks: `verify/sandwiched_supported.py`, `verify/theorem_c_context.py`
  (with `certificates/theorem_c_context.json`) and
  `verify/pentagon_numerical_bounds.py`; `verify/negative_controls.py` runs all
  six corruption tests.
- `tools/build.py` builds the paper cleanly; `requirements-tested.txt` pins the
  tested NumPy version.
- The SHA-256 digest in `certificates/README.md` is corrected, and the lemma
  numbers printed by `verify/entanglement_assisted_spectrum.py` match the
  manuscript. No computed value changed.

## 1.0.0 — 26 September 2026

First public release.
