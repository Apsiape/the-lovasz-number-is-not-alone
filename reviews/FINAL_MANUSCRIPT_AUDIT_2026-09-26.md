# Final-manuscript audit — 26 September 2026

## Scope

This audit compares Nidhal Mghirbi's proposed final rewrite with the previous
repository manuscript. It focuses on mathematical material new to the rewrite,
the exact-confusability appendix, claim wording, bibliography, reproducibility,
and rendered presentation. It does not repeat the complete QI-118/QI-120/QI-121
reconstructions or the exact certificate audit already recorded elsewhere.

## New mathematical material

### Sandwiched Rényi radii

The proposition

`tilde-vartheta_beta(G) = vartheta_{2-1/beta}(G)` for `beta in [1,infinity]`

passes reconstruction. For `theta=(beta-1)/beta`, set
`A=P sigma^{-theta} P` and `X=A^(1/2) rho A^(1/2)`. The constraint is
`Tr(A^(-1)X)=1`. Hölder with exponents `beta` and `1/theta` yields the claimed
lower bound, and `rho` proportional to `A^(-1/theta)` attains it. The
`beta=1` and max-relative endpoints agree with the supported Umegaki and shorted
operator formulas already used in the paper. Optimization therefore gives the
stated graph identity without an extra rank or dimension assumption.

### Exact confusability graphs

The edge-space perturbation correctly turns every permitted edge into a
nonzero overlap while preserving all nonedge orthogonalities. The submitted
dominator `(1-epsilon)T direct-sum epsilon Pi_E` did not dominate an isolated
vertex that the construction leaves unchanged. The manuscript now uses
`T direct-sum epsilon Pi_E`. It dominates every perturbed state, including
isolated vertices, and its trace still converges to `Tr T`. The Petz moments,
relative entropy, support weights, and order-one radius change continuously
under the same perturbation.

## Claims and sources

- The abstract now says “to our knowledge” before the statement that the
  Lovász number was the only previously known point of the
  entanglement-assisted spectrum.
- The Li--Zuiddam framing distinguishes the disproved “only point” route from
  the still-open minimal-element route.
- The Duan--Winter discussion uses the published IEEE equation numbering and
  does not extend the graph-level result to general noncommutative graphs.
- The incorrect Zenodo identifiers are absent. `Mghirbi2026` is identified as
  an unpublished manuscript under journal review, and the certificate recovery
  method is credited by description rather than unstable theorem numbers.
- The manuscript includes an explicit generative-AI disclosure that does not
  claim unaided human verification by either author. Responsibility for the
  submitted manuscript remains with the authors, while exact computational
  claims point to deterministic certificates and scripts.

## Finite controls and presentation

The final release must satisfy `python verify/run_all.py`; the three documented
perturbation modes must fail. The PDF must compile from the checked-in source,
have no unresolved references, and pass a complete rendered-page inspection.
Those release checks are recorded in the commit that adds this audit.

## Verdict

The rewrite is a substantial improvement in exposition and positioning. After
the dominator repair above, this audit found no new mathematical blocker. The
remaining publication risk is ordinary specialist scrutiny and the possibility
of missed priority literature, not a known gap in the final rewrite.
