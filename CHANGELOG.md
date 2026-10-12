# Changelog

## 1.2.0 — October 2026

A new main theorem and section; Theorems A–C, all certificate values and the numbering of
Sections 1–6 are unchanged.

- **Theorem D (order two is not the projective rank).** For the clone graph
  `G_1440 = F[(59, 60, 61, 63)]` of the magic-square seed,
  `Sigma(G_1440) <= 215940/899 < 14172/59 <= xi_f(complement of G_1440)`. Flat witnesses give
  `Sigma(G) <= xi_f(complement of G)` for every graph, and equality holds whenever `theta = alpha*`,
  on `C5` and on Duan and Winter's Hadamard example; Theorem D shows that it can fail. Version 1.1.1
  listed equality as an open problem.
- New Section 7, "Order two versus the projective rank": the flat bound (moved from the open problems),
  Proposition 7.1 (the order-two bridge for clone graphs is exact, `Sigma(F[k]) = 1/t_H(F[k])`),
  Lemma 7.2 (anticommutators bound traces), Lemma 7.3 (a rank inequality for the magic square, tight on
  the magic-square representation), the proof of Theorem D, and a paragraph on how the profile is
  chosen. Open problems become Section 8.
- Introduction: Theorem D with context; a "What is new" paragraph; the organization paragraph. The
  abstract gains one sentence and is tightened to stay within arXiv's limit.
- Open problems: "The projective rank" now records what Theorem D settles and what it leaves open
  (membership of the complement of the projective rank in the entanglement-assisted spectrum, exact
  values for `G_1440`, sharper inequalities, the smallest separating graph); "Above order two" notes
  that an extension reaching the projective rank would have to keep growing beyond order two.
- References: Ji (arXiv:1310.3794, Lemma 6, anticommutation in magic-square operator solutions) and
  Wocjan and Elphick (Electron. J. Combin. 26 (2019), rank-counting lower bounds on the projective rank).
- Verification: `verify/projective_rank_separation.py` and its pinned output; a seventh negative control.

## 1.1.1 — 30 September 2026

Attribution and framing corrections after an audit of how the paper credits other work, and
precision, citation and presentation fixes after a hostile referee audit, which found no false result
and no gap. No theorem, bound, certificate value or numbering changes; a few proofs gain a sentence
of precision.

- Dalai's Theorem 8 (due to Schrijver; IEEE Trans. Inf. Theory 59 (2013)) is credited as the identity
  `theta_0 = theta`, in the abstract, the introduction, Proposition 3.3 and Related work.
- Wang and Duan (ISIT 2016) answered Duan and Winter's question on strict submultiplicativity of
  `Sigma(K)`; Section 5 and the open problems now say so.
- Credits added: Duan, Severini and Winter for `Theta_* <= theta`; Duan and Winter's Theorems 2 and 5,
  their remarks anticipating Theorem A at order two, and their fixed-graph results (Proposition 18,
  Theorem 19); Shannon and Cubitt, Leung, Matthews and Winter for the fractional packing number; Li and
  Zuiddam (with Cubitt et al.) for Theorem A at order zero; Ohya, Petz and Watanabe; Beigi (sandwiched
  data processing); the classical spectral points.
- Wording made precise: the abstract's description of the spectrum and of `log_2 Sigma(G)` (an infimum,
  not an SDP value); Li and Zuiddam's suggestion (a proof route, not a question); the short pentagon
  proof (it also uses the projection formula); a heuristic in Section 7.
- Bibliography: Dalai's ISIT pages corrected; Li and Zuiddam's definition cited as Definition 7
  (Definition 6 in arXiv v2).

After the referee audit:

- Credits: `theta_0 = theta` is also credited to Duan and Winter (proof of their Theorem 5) and, for a
  pure center, to Cabello, Severini and Winter (arXiv:1010.2163), as noted by Dalai and Winter (IEEE
  Trans. Inf. Theory 63 (2017)). Related work states that Duan and Winter already express their
  fixed-channel quantities as radii (their Theorems 2 and 4). Vrana's interpolation with the Bukh–Cox
  value of the fractional Haemers bound already gives a continuum on `C5` in the ordinary spectrum;
  the introduction and Section 5.3 say that the new content is membership in the entanglement-assisted
  spectrum. Also credited or cited: Duan and Winter's fixed-cq-graph separation (Section IV.D); Li and
  Zuiddam's Theorem 22 (the fractional clique cover number is not in the quantum spectrum); Cubitt,
  Leung, Matthews and Winter (Phys. Rev. Lett. 104 (2010)) for the 24 magic-square vectors; Csiszár
  (1995); Cubitt et al.'s Definition 1; Vrana (2022) for uncountability; the concurrent works of
  Shariat, Hoogsteder-Riera and Tomamichel and of Cheng and Berta; Oufkir, Tomamichel and Berta;
  Pisier and Xu for interpolation of Schatten classes.
- Data availability: a back-matter section "Data and code availability" (Zenodo concept DOI and
  GitHub); "Reproducibility" and "AI-assisted tools" move to the back matter; repository paths in the
  text are replaced by script names.
- Theorem C is checkable from the paper: Section 6.5 prints the Gibbs witnesses (centers proportional
  to `diag(A^4, B^4, B^4, B^4)` with `(A, B) = (41, 56), (56, 51), (3, 4)`, plus clique blocks), the
  bounds are also given as exact rationals, equation (14) is labelled as certified bounds, and
  Appendix A states how identically vanishing moments are treated and that the integer positivity
  recipe factors `Z - gamma I`. `certificates/README.md` documents the data format.
- Precision: the family is called monotone rather than one continuous curve (continuity is proved on
  `[0, 1)`, right continuity on `[0, 2)`); Remark 4.8 says where the argument stops and that
  Proposition 3.1, Lemma 3.6 and Lemmas 4.3–4.4 hold above order two; complex orthonormal
  representations are realified before Lovász's results are applied; Lemma 4.4 assumes nonzero
  projections; Lemma 5.4 interpolates Schatten classes only; the proof of Theorem 5.5 notes that
  averaging loses nothing; the support convention for a non-faithful second argument, `K_s` for
  positive definite operators, the null graph and the basis for the transpose are stated; a remark
  after Proposition 3.5 treats pure states; an unnumbered remark in Section 7 bounds every
  `theta_alpha` by the projective rank of the complement; several local wordings are corrected.
- Figure 1 draws the value 5/2 on `[0.122, 1/2]` dashed, since there it is only an upper bound, and its
  caption quotes `2.44084 < 2.44521` (the witness radius was rounded down before);
  `verify/pentagon_numerical_bounds.py` checks the new caption. Table 1's last column is "certified
  gap >= (bits)", with the G44 entry rounded down to 0.002145. No plotted coordinate changes.
- `verify/small_graph_separation.py` now prints each certified bound rounded in its safe direction
  (upper bounds up, lower bounds down); its pinned output changes in three digits accordingly.
- The abstract is shortened to fit arXiv's limit, and it now says that `log_2 theta`, `C_min` and
  `log_2 Sigma` are the radii.

## 1.1.0 — 30 September 2026

Theorems A–C, every certificate value and the numbering of version 1.0.0 are
unchanged; the one new lemma is placed last (Lemma B.2).

### Mathematics

- **Proposition 3.5** now proves
  `sandwiched_theta_beta(G) = theta_{2-1/beta}(G)` for the whole range
  `1/2 <= beta <= infinity` (version 1.0.0: `beta >= 1`). The sub-one argument
  uses an isometric reduction to a compressed moment, pinching and scalar
  Hölder, and gives an explicit minimizer faithful on the prescribed support.
  The endpoints `1/2`, `1` and `infinity` are treated directly, and no limit is
  exchanged with an unbounded-dimension infimum. Frank–Lieb (2013) is cited
  for data processing of the sandwiched family.
- **Correction.** Figure 4 and Section 7 of version 1.0.0 stated that both
  illustrated pentagon geometries are nonoptimal throughout `0 < alpha < 1/2`;
  the displayed bounds do not establish this. Version 1.1.0 states the proved
  regimes (the flat witness is optimal on `[1/2, 2]`; the umbrella attains the
  order-zero value) and leaves the intermediate graph value open. The captions
  of Figures 1 and 4 distinguish the limiting handle-center witness from an
  optimized center, and the crossing of two upper bounds from a transition in
  the graph value.

### Exposition

- Section 5.4 quotes Duan and Winter's definitions of `Sigma(G)` and
  `S_0,NS(G)`, their Lemma 23, the remark after their chain and their pentagon
  conjecture (from arXiv:1409.3426v3, which numbers the chain (53) instead of
  the journal's (54)), and explains why their Proposition 18 does not give the
  graph-level single-letter formula.
- Appendix B.4 (Lemma B.2) derives equations (9)–(10) from Li and Zuiddam's
  Definition 7 (Definition 6 in arXiv v2) and their complement convention.
- Figure 1 adds numerical upper bounds on `theta_alpha(C5)` for
  `0.04 <= alpha <= 0.125` from explicit witnesses (umbrella vectors with an
  optimized faithful center): 2.4408 < 2.4452 at `alpha = 0.1`, below 5/2 until
  `alpha` is about 0.128. The shaded band and all curves are unchanged.
- Theorem C is followed by `theta = 6, 8, 12` and `alpha* = 32/5, 37/4, 72/5`
  for G32, G44, G72, and the smallest eigenvalues of the dual matrices.
- Every cross-reference carries an explicit type, so references print with the
  correct name under any TeX distribution.

### Package

- New checks: `verify/sandwiched_supported.py`, `verify/theorem_c_context.py`
  (with `certificates/theorem_c_context.json`) and
  `verify/pentagon_numerical_bounds.py`; `verify/negative_controls.py` runs all
  six corruption tests.
- `tools/build.py` builds the paper cleanly; `requirements-tested.txt` pins the
  tested NumPy version.
- The SHA-256 digest in `certificates/README.md` is corrected, and the lemma
  numbers printed by `verify/entanglement_assisted_spectrum.py` match the
  manuscript. No computed value changed.

## 1.0.0 — 26 September 2026

First public release.
