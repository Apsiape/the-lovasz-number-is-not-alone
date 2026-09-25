# Version-1 review checklist

This file records what must be checked before public circulation.  Script
success is not a promotion of any theorem.

## Mathematical gates

- [ ] Reconstruct supported Petz minimization for positive, zero, and negative
      compression powers, including the order-zero support convention.
- [ ] Reconstruct the normalized tower identity and the row-span extraction
      for an arbitrary joint strong-product representation.
- [ ] Check the orthogonal-sum inequality used for disjoint-union additivity.
- [ ] Check the flagged-mixture argument and Petz data processing at both
      endpoints `alpha=0,2`.
- [ ] Check the complement convention in the entanglement-assisted preorder.
- [ ] Reconstruct the two endpoint operator bounds and the three-lines
      interpolation for the pentagon.
- [ ] Check every inequality in the infinite distinctness ladder.
- [ ] Reconstruct the harmonic vector-state moment model without imposing any
      orthogonality relation on the auxiliary projections.
- [ ] Check the direct bridge from a common dominator to the harmonic bound and
      from the Gibbs witness to the information-radius bound.
- [ ] Independently inspect the certificate key reductions and the exact
      positive-semidefinite proof.

## Literature gates

- [x] Search for post-2020 points of the entanglement-assisted asymptotic
      spectrum beyond the Lovász number.
- [x] Compare carefully with fractional Haemers bounds: Li--Zuiddam place them
      in the quantum spectrum, not automatically in the stronger
      entanglement-assisted spectrum.
- [x] Compare with Vrana's probabilistic refinements and identify whether any
      specialization already equals the present family.
- [x] Check Rényi/Augustin graph-radius and sphere-packing literature for an
      equivalent graph-level optimization.
- [x] Verify the precise novelty claim for graph-level multiplicativity of
      `Sigma` against work following Duan--Winter.

The search record and the resulting qualifications are in
`LITERATURE_AUDIT.md`.  These boxes record completion of the search, not a
mathematical proof audit or an absolute guarantee against missed literature.

## Claims deliberately not made

- The Lovász number is not shown to be nonminimal in the spectrum.
- Entanglement-assisted Shannon capacity is not identified with any new point.
- Orders above two are not covered.
- Uncountably many distinct points are not proved.
- The exact pentagon curve on `(0,1/2)` is not determined.
- The 32-vertex graph is not proved minimal.
- The exact values of its endpoint parameters are not computed.

## Deterministic controls

Run:

```powershell
python verify/run_all.py
python verify/entanglement_assisted_spectrum.py --perturb
python verify/small_graph_separation.py --perturb
python verify/small_graph_separation.py --perturb-psd
```

The first command must exit zero.  Each of the remaining three commands must
exit nonzero.  They respectively damage the pentagon ladder, an affine moment
equation, and positivity while leaving the affine equations intact.
