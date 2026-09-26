# The Lovász number is not alone

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22983499.svg)](https://doi.org/10.5281/zenodo.22983499)

This repository contains the paper

> **The Lovász number is not alone: a continuum of Rényi points in the entanglement-assisted spectrum of graphs**
>
> Nidhal Mghirbi and Seth Douglas

We minimize Petz--Rényi information radii over classical--quantum channels
compatible with a graph. The resulting parameters form a continuum of points
in Li and Zuiddam's entanglement-assisted asymptotic spectrum. The paper also
proves strong-product multiplicativity for arbitrary joint representations,
resolves the Duan--Winter pentagon conjecture, shows that graph-level
no-signalling simulation single-letterizes, and gives an exact rational
certificate for a 32-vertex graph with
`C_min(G) < log_2 Sigma(G)`.

## Repository layout

- `paper/main.tex` -- standalone manuscript.
- `paper/references.bib` -- primary references.
- `output/pdf/the-lovasz-number-is-not-alone-v1.pdf` -- latest visually reviewed
  manuscript build.
- `certificates/` -- exact rational certificate data for the 32-, 44-, and
  72-vertex examples.
- `verify/` -- deterministic certificate checks and pinned output.
- `CITATION.cff` -- citation metadata.
- `LICENSE.md` -- licensing for the manuscript, data, and verification code.

## Build the paper

From the repository root:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd paper/main.tex
```

The PDF is written to `paper/main.pdf`.

## Verify the finite certificates

Python 3 and NumPy are required.

```powershell
python -m pip install -r requirements.txt
python verify/run_all.py
```

The exact small-graph checker verifies the rational affine equations and the
positive-semidefinite certificate using integer arithmetic. Floating-point
Cholesky factorization is used only to propose an integer factor; it is not an
acceptance criterion.

The following negative controls are expected to exit unsuccessfully:

```powershell
python verify/entanglement_assisted_spectrum.py --perturb
python verify/small_graph_separation.py --perturb
python verify/small_graph_separation.py --perturb-psd
```

Passing the scripts establishes only the stated finite algebraic checks. It is
not a substitute for reviewing the dimension-independent arguments.

## Citation and license

The archived `v1.0.0` release is available at
[10.5281/zenodo.22983499](https://doi.org/10.5281/zenodo.22983499). The
all-versions concept DOI is
[10.5281/zenodo.22983498](https://doi.org/10.5281/zenodo.22983498). Citation
metadata are in `CITATION.cff`.

The manuscript and certificate data are released under CC BY 4.0; the
verification software is released under the MIT License. See `LICENSE.md` for
the scope and full notices.
