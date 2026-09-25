# Literature and priority audit

**Date:** 2026-09-25  
**Scope:** novelty of the Petz--Rényi spectral family, its pentagon
separation, arbitrary-joint product theorem, and the 32-vertex endpoint
separation.

This is a search record, not a mathematical validation of the manuscript.
It should be revisited after expert circulation and before any categorical
"first" claim in a journal submission.

## Search performed

The audit used title/phrase searches across arXiv and general scholarly web
indexes for combinations of `entanglement-assisted asymptotic spectrum`,
`Petz`, `Rényi`, `Augustin`, `information radius`, `Lovasz theta`, graph
simulation cost, and the notation used by Li--Zuiddam.  It also inspected the
works indexed by OpenAlex as citing Li--Zuiddam's paper (six records as of the
audit date), and read the relevant parts of the following primary sources:

- [Li--Zuiddam, *Quantum asymptotic spectra of graphs and non-commutative
  graphs, and quantum Shannon capacities*](https://arxiv.org/abs/1810.00744).
- [Dalai, *Lovász's Theta Function, Rényi's Divergence and the
  Sphere-Packing Bound*](https://arxiv.org/abs/1301.6339).
- [Vrana, *Probabilistic refinement of the asymptotic spectrum of
  graphs*](https://arxiv.org/abs/1903.01857).
- [Duan--Winter, *No-Signalling Assisted Zero-Error Capacity of Quantum
  Channels and an Information Theoretic Interpretation of the Lovasz
  Number*](https://arxiv.org/abs/1409.3426).
- [Gao--Gribling--Li, *On a tracial version of Haemers
  bound*](https://arxiv.org/abs/2107.02567).
- [Wang--Duan, *On the quantum no-signalling assisted zero-error classical
  simulation cost of non-commutative bipartite
  graphs*](https://arxiv.org/abs/1601.06855).

## Findings

### 1. Entanglement-assisted spectral points

Li and Zuiddam proved that the Lovász number belongs to
`X(G, <=_*)`, wrote that they had found no other element, and explicitly
raised the possibility that it could be the only point.  Their other graph
parameters--fractional real/complex Haemers bounds and projective rank--were
placed in the weaker quantum spectrum `X(G, <=_q)`; they state that the
corresponding entanglement-assisted monotonicity was unknown.

The post-2020 search found no paper constructing another point of the graph
entanglement-assisted spectrum.  Gao--Gribling--Li construct tracial rank and
tracial Haemers points for the commuting-quantum spectrum, not for
`X(G, <=_*)`.

**Priority assessment:** subject to proof review, the spectral-point theorem
is very likely the first explicit construction beyond Lovász theta in
`X(G, <=_*)`; the pentagon theorem is then the first explicit infinite family
of pairwise distinct points there.  This is the paper's principal novelty.

### 2. Dalai and Augustin/Rényi radii

Dalai gives the closest conceptual precursor.  He expresses cq sphere-packing
bounds through Petz/Csiszar Rényi information radii and recovers the Lovász
number at the zero-error endpoint after optimizing graph representations.
He does not prove that the finite-order graph optimizations are additive,
strong-product multiplicative, or monotone for the entanglement-assisted
cohomomorphism preorder.  General Augustin-capacity work studies a fixed
channel rather than this graph optimization.

**Priority assessment:** the manuscript must present the family as a new
spectral theorem built from known information-radius ingredients, not as the
first connection between Rényi divergence and Lovász theta.

### 3. Vrana's probabilistic refinements

Vrana proves that every scalar point of the ordinary graph asymptotic
spectrum has a probability-distribution refinement.  The construction starts
from an already available scalar point, and the monotonicity is for the
ordinary cohomomorphism preorder.  It neither supplies a new scalar point of
the entanglement-assisted spectrum nor specializes to the present
graph-optimized Petz family without first proving the missing scalar spectral
theorem.

### 4. Product multiplicativity and the order-two endpoint

Duan--Winter already prove multiplicativity of `Sigma(K)` for two fixed
cq-graphs.  Wang--Duan extends the surrounding noncommutative-bipartite-graph
analysis.  Therefore multiplicativity of fixed-channel/cq-graph simulation
cost is not new.

The manuscript's product theorem has a stronger graph-optimization
quantifier: a compatible representation of `G strong-product H` may be an
arbitrary joint representation, not the tensor product of witnesses for `G`
and `H`.  The nested-compression lower bound is the novel step that prevents
the graph infimum from evading fixed-representation multiplicativity.

### 5. The 32-vertex endpoint separation

Duan--Winter already exhibit fixed cq-channels for which an entropic capacity
is strictly below exact simulation cost.  That does not imply a separation
after minimizing both quantities over every representation compatible with a
single classical graph.  The audit found no earlier graph-level example of
`C_min(G) < log_2 Sigma(G)`.

**Priority assessment:** the 32-vertex certificate appears novel and is a
strong endpoint witness, but it is supporting rather than the headline
result.  The paper does not claim that 32 vertices is minimal.

## Recommended public claim

The defensible introduction-level statement is:

> To our knowledge, this is the first construction of spectral points beyond
> the Lovász number in the entanglement-assisted asymptotic spectrum of
> graphs, and hence the first infinite family of points in that spectrum.

Do not say that the work introduces Rényi graph radii, proves fixed-cq
simulation multiplicativity for the first time, or gives the first
channel-level gap between capacity and simulation cost.

## Residual uncertainty

- Citation indexes are incomplete and terminology varies; an expert in
  quantum graph homomorphisms should still be asked specifically about the
  first-point claim.
- The exact relation between the order-one endpoint and earlier
  noncommutative-bipartite-graph formulations deserves a line-by-line proof
  comparison during mathematical review.
- No priority search can validate the nested-compression, EA monotonicity,
  pentagon, or finite-certificate arguments.  Those remain the open items in
  `REVIEW.md`.
