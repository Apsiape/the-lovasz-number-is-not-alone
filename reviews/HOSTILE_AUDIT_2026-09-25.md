# Blind hostile proof audit

**Date:** 2026-09-25  
**Auditor:** independent GPT-5.6-sol task with no inherited conversation
context  
**Status:** mathematical review record; not a substitute for human refereeing

## Verdict

The headline spectral theorem survives.  The auditor independently
reconstructed the arbitrary-joint strong-product lower bound and the
entanglement-assisted monotonicity proof, including the endpoint orders.  It
found no substantive counterexample or missing hypothesis in either argument.
The pentagon ladder and the exact 32-vertex endpoint separation also survived.

The draft nevertheless required local repair before circulation.  In
particular, the defining display omitted `Tr sigma = 1`; read literally, free
positive scaling would trivialize the radius.  The intended density-operator
normalization was used everywhere else.  The revision associated with this
record makes that condition explicit and also:

- states the ambient support used in recursive power compression;
- dispatches empty-graph cases;
- proves one-vertex normalization directly;
- expands the direct-sum construction that splits parent supports into clones;
- explains the vertex-transitive block symmetrization; and
- initially removed an unqualified order-three counterexample assertion that
  was not proved exactly in the manuscript.  The later revision restores it
  only as a clearly labeled deterministic numerical witness from the verifier.

## Load-bearing results

| Result | Verdict | Principal hostile check |
|---|---|---|
| Supported-state variational and packing formulas | Pass | Checked all orders, support restrictions, and absence of a minimax exchange. |
| Tower identity | Pass | Tested negative compression powers and noncommuting nested supports. |
| Arbitrary-joint strong-product theorem | Pass | Reconstructed the row-span packing argument without a product representation or optimizer. |
| Orthogonal-sum and disjoint-union theorems | Pass | Checked the scalar convexity directions throughout `s in [-1,1]`. |
| Flagged-mixture lemma | Pass | Checked singular assistance, noncommuting blocks, Petz DPI endpoints, and the direct order-zero support argument. |
| Entanglement-assisted monotonicity | Pass | Compared the nonedge/equal-or-adjacent condition with Li--Zuiddam's complement convention. |
| Pentagon inequalities and infinite ladder | Pass | Checked arbitrary-rank noncommuting packings and interpolation constants. |
| Operational bridge and harmonic relaxation | Pass after exposition repair | Reconstructed clone splitting by a finite direct sum and harmonic superadditivity by Schur complements. |
| Exact 32-vertex certificate | Pass | Exact affine system and PSD certificate verified; negative controls rejected. |

## Strongest attempted falsifiers

For multiplicativity, the auditor used a nonfactor, noncommuting joint packing
at negative compression power, where ordinary compression and inversion do
not commute.  The exact nested operation still collapses to
`P sigma^s P`, so the tower argument survives.

For entanglement-assisted monotonicity, it allowed singular assistance and
fully noncommuting decomposition operators.  Restriction to the assistance
support, classical flagging, Petz data processing through order two, and the
direct order-zero support inequality still give the claimed direction.

## Remaining publication gates

This audit did not replace specialist human review.  Before public submission,
the proof should still be read independently by an expert in quantum graph
homomorphisms/asymptotic spectra, and all external standard dependencies listed
in the manuscript should be checked for precise hypotheses and citations.
