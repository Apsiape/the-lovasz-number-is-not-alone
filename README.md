# Petz--Rényi graph spectrum

This private repository contains the working paper

> **A Rényi family in the entanglement-assisted asymptotic spectrum of graphs**
> Seth Douglas and Nidhal Mghirbi

The paper studies graph parameters obtained by minimizing Petz--Rényi
information radii over compatible classical--quantum channels.  Its main
candidate results are:

1. for every order `alpha` in `[0,2]`, the resulting parameter is a point of
   Li and Zuiddam's entanglement-assisted asymptotic spectrum of graphs;
2. the pentagon distinguishes infinitely many orders;
3. nested compression proves strong-product multiplicativity for arbitrary
   joint representations, rather than only for product witnesses; and
4. exact rational moment certificates give a 32-vertex graph with
   `C_min(G) < log_2 Sigma(G)`.

This is a **version-1 research draft**.  The theorem statements and exact
certificates have been reconstructed.  A dated literature/priority audit and
a blind hostile proof audit are recorded in the repository.  Specialist human
review remains outstanding.  The manuscript does not claim an exact
entanglement-assisted Shannon-capacity formula, a complete description of the
spectrum, or an exact intermediate reliability curve.

## Repository layout

- `paper/main.tex` -- standalone manuscript.
- `paper/references.bib` -- primary references.
- `output/pdf/petz-renyi-graph-spectrum-v1.pdf` -- latest visually reviewed
  manuscript build.
- `certificates/` -- exact rational certificate data for the 32-, 44-, and
  72-vertex examples.
- `verify/` -- deterministic checks and pinned output.
- `REVIEW.md` -- proof-audit and literature-audit checklist.
- `LITERATURE_AUDIT.md` -- dated novelty search, closest prior art, and
  claim-by-claim priority assessment.
- `reviews/HOSTILE_AUDIT_2026-09-25.md` -- independent adversarial proof audit,
  attempted falsifiers, repairs, and publication verdict.

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
positive-semidefinite certificate using integer arithmetic.  Floating-point
Cholesky factorization is used only to propose an integer factor; it is not an
acceptance criterion.  Negative-control modes are documented in `REVIEW.md`.

## Status discipline

The manuscript distinguishes proved implications from computational
certification and from open questions.  Passing the scripts establishes only
the stated finite algebraic checks.  It is not a substitute for reviewing the
dimension-independent arguments.
