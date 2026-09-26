# The Lovász number is not alone

This private repository contains the working paper

> **The Lovász number is not alone: a continuum of Rényi points in the entanglement-assisted spectrum of graphs**
> Nidhal Mghirbi and Seth Douglas

The paper studies graph parameters obtained by minimizing Petz--Rényi
information radii over compatible classical--quantum channels.  Its main
candidate results are:

1. for every order `alpha` in `[0,2]`, the resulting parameter is a point of
   Li and Zuiddam's entanglement-assisted asymptotic spectrum of graphs;
2. order-continuity makes the pentagon distinguish a continuum of points,
   with values filling `[sqrt(5), 5/2]` before the exact plateau;
3. nested compression proves strong-product multiplicativity for arbitrary
   joint representations, rather than only for product witnesses; and
4. graph-level multiplicativity of `Sigma` resolves the Duan--Winter pentagon
   conjecture and removes the regularization in graph no-signalling simulation;
5. exact rational moment certificates give a 32-vertex graph with
   `C_min(G) < log_2 Sigma(G)`.
6. optimizing sandwiched Rényi radii of orders `beta >= 1` gives the same
   curve as the Petz family on orders `[1,2]`.

This is a **preprint candidate**.  The theorem statements and exact
certificates have been reconstructed, and Nidhal Mghirbi reports a complete
author-side proof review.  Dated literature/priority and hostile proof audits
are recorded in the repository.  The manuscript does not claim an exact
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
- `reviews/CONTINUUM_DUAN_WINTER_AUDIT_2026-09-25.md` -- focused hostile audit
  of the continuum argument and the Duan--Winter model identification.
- `reviews/FINAL_MANUSCRIPT_AUDIT_2026-09-26.md` -- audit of the final rewrite,
  its new sandwiched-radius proposition, exact-confusability appendix, and
  disclosure/provenance changes.

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
