# Focused hostile audit: continuum and Duan--Winter chain

**Date:** 2026-09-25
**Scope:** only the new order-continuity argument, the continuum conclusion,
and the identification with the published Duan--Winter graph simulation
model.  This record does not reopen every proof in the manuscript.

## Verdict

Both additions survive the audit.  The continuity proof is dimension-uniform
and passes through the graph infimum; it does not assume a common optimizer or
compactness of the set of all representations.  The order-two product theorem
uses the same graph-level common-dominator optimization that Duan and Winter
regularize, so it removes the regularization and proves their pentagon
equalities.

## 1. Order continuity

For a fixed finite witness with faithful center, each Petz divergence is
right-continuous in the order on `[0,1)`.  A witness within `eta` of the graph
infimum therefore gives the required right upper limit; monotonicity gives the
other direction.  This avoids any assertion that an optimizer exists.

The delicate direction is left continuity.  For `0 < beta < alpha < 1`,
convexity of

`psi(t) = log Tr rho^t sigma^(1-t)`

and `psi(0) <= 0 = psi(1)` imply

`D_alpha <= alpha(1-beta)/(beta(1-alpha)) D_beta`.

The multiplier is independent of dimension, state, and representation.
Consequently it survives the maximum over vertices and the infimum over all
compatible finite-dimensional representations.  Together with monotonicity,
the multiplier tending to one as `beta` approaches `alpha` proves left
continuity.  A merely witness-by-witness continuity statement would not have
been enough; the manuscript now states the uniform comparison explicitly.

Since the pentagon values at orders zero and one half are `sqrt(5)` and
`5/2`, continuity and monotonicity make the image of `[0,1/2]` exactly that
interval.  Different evaluations on one graph certify different spectral
functions, so the continuum conclusion follows.

## 2. Duan--Winter model match

The published IEEE version defines the graph quantity by minimizing the
fractional common-dominator simulation cost over compatible cq
representations, then regularizing it over strong graph powers.  This is the
same `Sigma` and the same graph optimization used in the manuscript.  The
published equation number is (54); the arXiv numbering differs.

Duan--Winter's fixed-cq-graph multiplicativity does not by itself commute with
the graph representation infimum.  The manuscript's arbitrary-joint product
theorem supplies exactly that missing quantifier at order two.  Therefore
`S_{0,NS}(G) = log_2 Sigma(G)` for classical graphs.  This statement does not
settle the authors' broader question for general noncommutative graphs and is
not advertised as an efficient computation of `Sigma`.

For `C5`, the endpoint identities and the proved plateau give both
`C_min(C5)` and `log_2 Sigma(C5)` equal to `log_2(5/2)`.  The fractional
independence number of the five-cycle is `5/2`, while its Lovász number is
`sqrt(5)`.  Thus the conjectured non-Lovász equalities hold and the leftmost
inequality in the published chain is strict.

## 3. Priority and residual risk

A focused exact-phrase search and an OpenAlex forward-citation scan found no
earlier Rényi continuum in the entanglement-assisted graph spectrum and no
later paper claiming the Duan--Winter pentagon equality chain.  This is
evidence, not an exhaustive guarantee.  The first-point and open-problem
claims remain phrased as “to our knowledge,” and specialist human review is
still recommended before public posting.

The audit also checked that the revision does **not** claim:

- that Lovász theta fails to be the least spectral point;
- that the pentagon curve below order one half is known exactly;
- that the definition or EA monotonicity extends beyond Petz order two;
- that graph-level single-letter characterization is an algorithm; or
- that the noncommutative-graph multiplicativity question is resolved.
