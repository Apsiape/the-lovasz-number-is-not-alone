# Version-1 review checklist

This file records what must be checked before public circulation.  Script
success is not a promotion of any theorem.

## Mathematical gates

- [x] Reconstruct supported Petz minimization for positive, zero, and negative
      compression powers, including the order-zero support convention.
- [x] Reconstruct the normalized tower identity and the row-span extraction
      for an arbitrary joint strong-product representation.
- [x] Check the orthogonal-sum inequality used for disjoint-union additivity.
- [x] Check the flagged-mixture argument and Petz data processing at both
      endpoints `alpha=0,2`.
- [x] Check the complement convention in the entanglement-assisted preorder.
- [x] Reconstruct the two endpoint operator bounds and the three-lines
      interpolation for the pentagon.
- [x] Check every inequality in the infinite distinctness ladder.
- [x] Check the graph-uniform transfer in the order-continuity proof and the
      endpoint-to-continuum argument on the pentagon.
- [x] Match the graph optimization, product, and regularization conventions
      to the published Duan--Winter model and Eq. (54).
- [x] Reconstruct the harmonic vector-state moment model without imposing any
      orthogonality relation on the auxiliary projections.
- [x] Check the direct bridge from a common dominator to the harmonic bound and
      from the Gibbs witness to the information-radius bound.
- [x] Independently inspect the certificate key reductions and the exact
      positive-semidefinite proof.
- [x] Reconstruct the supported-state minimization identifying optimized
      sandwiched order `beta` with Petz order `2-1/beta`, including the
      max-relative endpoint.
- [x] Check the exact-confusability perturbation and repair its common
      dominator so that isolated vertices remain dominated.

These boxes record the blind hostile audit dated 2026-09-25.  Its scope,
attempted falsifiers, repairs, and remaining human-review requirement are in
`reviews/HOSTILE_AUDIT_2026-09-25.md`.

The last two boxes record the focused final-manuscript audit dated 2026-09-26.
Nidhal Mghirbi separately reports having checked every proof in the manuscript.

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
- [x] Re-scan forward citations of Li--Zuiddam and Duan--Winter for another
      EA spectral continuum or a published resolution of the pentagon
      conjecture.
- [x] Verify that the final bibliography uses the published Duan--Winter
      equation numbering and removes the erroneous Zenodo identifiers for the
      unpublished certificate-recovery manuscript.

The search record and the resulting qualifications are in
`LITERATURE_AUDIT.md`.  These boxes record completion of the search, not a
mathematical proof audit or an absolute guarantee against missed literature.

## Claims deliberately not made

- Entanglement-assisted Shannon capacity is not identified with any new point.
- Orders above two are not covered.
- The exact pentagon curve on `(0,1/2)` is not determined.
- The Lovász number is not shown to be the least spectral point; only the
  stronger "only point" possibility is ruled out.
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
