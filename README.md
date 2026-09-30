# The Lovász number is not alone

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22983498.svg)](https://doi.org/10.5281/zenodo.22983498)

This repository contains the paper

> **The Lovász number is not alone: a continuum of Rényi points in the entanglement-assisted spectrum of graphs**
>
> Nidhal Mghirbi and Seth Douglas

We minimize Petz--Rényi information radii over classical--quantum channels
compatible with a graph. The resulting parameters form a continuum of points
in Li and Zuiddam's entanglement-assisted asymptotic spectrum. Sandwiched
Rényi radii of every order `beta` in `[1/2, infinity]` give exactly the same
points, at Petz order `2 - 1/beta`, so one curve runs from the Lovász number
to the no-signalling simulation cost. The paper also proves strong-product
multiplicativity for arbitrary joint representations, resolves the
Duan--Winter pentagon conjecture, shows that graph-level no-signalling
simulation single-letterizes, and gives an exact rational certificate for a
32-vertex graph with `C_min(G) < log_2 Sigma(G)`.

## What is new in version 1.1

- The correspondence between sandwiched and Petz radii (Proposition 3.5) now
  covers the whole range `1/2 <= beta <= infinity`, with explicit minimizers.
  Version 1.0 proved it above order one.
- **Correction.** Version 1.0 stated that both pentagon geometries shown in
  Figure 4 are nonoptimal throughout `0 < alpha < 1/2`. The displayed bounds
  do not show this. Version 1.1 states only the proved regimes: the flat
  witness is optimal on `[1/2, 2]`, and the umbrella attains the order-zero
  value. Figure 1 adds numerical upper bounds for small `alpha` from explicit
  witnesses.
- Section 5.4 quotes Duan and Winter's definitions, their Lemma 23 and their
  pentagon conjecture, and explains why their fixed-channel multiplicativity
  does not give the graph-level single-letter formula. Appendix B.4 derives
  the preorder used in Section 2.3 from Li and Zuiddam's definition.
- Theorem C is placed in context (Lovász numbers, fractional packing numbers
  and the margins of the dual matrices of the three certified graphs).

Theorems A--C, all certificate values and the numbering of version 1.0 are
unchanged. See [CHANGELOG.md](CHANGELOG.md).

## Repository layout

- `paper/main.tex` -- standalone manuscript.
- `paper/references.bib` -- primary references.
- `output/pdf/the-lovasz-number-is-not-alone-v1.1.pdf` -- manuscript build.
- `certificates/` -- exact rational certificate data for the 32-, 44-, and
  72-vertex examples, and exact data for the context of Theorem C.
- `verify/` -- deterministic checks and their pinned output.
- `tools/build.py` -- clean pdfLaTeX/BibTeX build.
- `CITATION.cff` -- citation metadata.
- `LICENSE.md` -- licensing for the manuscript, data, and verification code.

## Build the paper

A TeX distribution with pdfLaTeX, BibTeX and the packages listed in
`paper/main.tex` is required; all figures are TikZ/PGFPlots source. From the
repository root:

```sh
python tools/build.py
```

This writes `output/pdf/the-lovasz-number-is-not-alone-v1.1.pdf` and the logs
to `output/build/`. The usual latexmk workflow also works and writes
`paper/main.pdf`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex
```

## Verify

Python 3 and NumPy are required; `requirements-tested.txt` pins the version
with which every check was run.

```sh
python -m pip install -r requirements.txt
python verify/run_all.py
```

The runner executes every script in `verify/` and compares its output with the
pinned copy in `verify/expected/`:

- `small_graph_separation.py` checks the rational affine equations and the
  positive-semidefinite certificates of Theorem C in integer arithmetic.
  Floating-point Cholesky factorization only proposes an integer factor; it is
  not an acceptance criterion.
- `entanglement_assisted_spectrum.py` checks the pentagon distinctness ladder
  and the rational separation in exact arithmetic, and runs finite numerical
  controls of Lemmas 4.3–4.6, Theorem 4.7 and the pentagon bounds of Section 5.
- `theorem_c_context.py` checks the Lovász numbers and fractional packing
  numbers of the three graphs in exact rational arithmetic.
- `sandwiched_supported.py` is a deterministic numerical regression for the
  supported minimum of Proposition 3.5 (seed `20260929`, tolerance `1e-8`).
- `pentagon_numerical_bounds.py` rebuilds each numerical witness of Figure 1.
- `negative_controls.py` runs six corruption tests and requires each to be
  rejected with its specific diagnostic:

```sh
python verify/entanglement_assisted_spectrum.py --perturb
python verify/small_graph_separation.py --perturb
python verify/small_graph_separation.py --perturb-psd
python verify/sandwiched_supported.py --perturb
python verify/theorem_c_context.py --perturb
python verify/pentagon_numerical_bounds.py --perturb
```

Passing the scripts establishes only the stated finite checks. The
dimension-independent statements are proved in the paper.

## Citation and license

The all-versions concept DOI
[10.5281/zenodo.22983498](https://doi.org/10.5281/zenodo.22983498) resolves to
the latest version. The `v1.0.0` archive is
[10.5281/zenodo.22983499](https://doi.org/10.5281/zenodo.22983499). Citation
metadata are in `CITATION.cff`.

The manuscript and certificate data are released under CC BY 4.0; the
verification software and build helper are released under the MIT License.
See `LICENSE.md` for the scope and full notices.
