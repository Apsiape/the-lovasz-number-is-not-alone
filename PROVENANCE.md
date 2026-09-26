# Provenance

This repository is a paper repository, not a research-return archive. It
contains the proof narrative and the minimum certificate bundle needed to
reproduce the finite claims.

The V1 manuscript was consolidated on 2026-09-25 from the following internal
research records in `Apsiape/quantum-interfaces-lab`:

- QI-118: entanglement-assisted Petz--Renyi spectral points;
- QI-121: independent product audit and supported-state bridge;
- QI-120: the 32-, 44-, and 72-vertex endpoint certificates;
- the independent small-graph reconstruction and verifier audit;
- the earlier QI-70/QI-73/QI-74 pentagon and endpoint notes.

The 2026-09-25 revision adds the graph-uniform continuity argument distilled
from QI-74, the resulting continuum theorem, and the Duan--Winter pentagon
corollary obtained by combining the order-two endpoint with arbitrary-joint
graph multiplicativity.  It also incorporates Nidhal Mghirbi's corrected
manuscript citation and explicit credit for the certificate recovery method.

The exact certificate data and deterministic verification scripts were copied
without mathematical modification. The only path-level adjustment is that
`verify/small_graph_separation.py` reads the certificate from
`certificates/small_graph_certificates.json`.

Certificate data SHA-256:

```text
0ed543d81d5a14d569ac5711f534ced19ca3e1a910d91c606f48e53a66075f7a
```

The repository intentionally omits raw commission transcripts, broad project
ledgers, and unrelated exploratory work.

## Final-manuscript rewrite, 2026-09-26

Nidhal Mghirbi supplied a complete rewrite of the manuscript and bibliography,
including the present title, figures, theorem-level narrative, the sandwiched
Rényi-radius identification, and the exact-confusability appendix.  The source
files and rendered PDF received for this revision had SHA-256 hashes:

```text
main.tex     6aa1a3e08f186c2eb6a417bdd311861e35994fce2614ae066828ed26f9e4ff64
references.bib d28057c0f15984257c9e9922a202d41feb0a859efdb68fb47f5286da1d1fcc46
proposal PDF 87cb7b1da5b133265fb615c8b45a24a45bdd86994bba863615043bbcbf959057
```

The repository version makes three documented editorial changes after that
intake: it qualifies the abstract's literature statement with “to our
knowledge,” repairs the common dominator in the exact-confusability lemma from
`(1-epsilon)T` to `T`, and adds a disclosure of generative-AI assistance.  The
mathematical audit of the new material is recorded in
`reviews/FINAL_MANUSCRIPT_AUDIT_2026-09-26.md`.

The rebuilt 23-page release PDF at
`output/pdf/petz-renyi-graph-spectrum-v1.pdf` has SHA-256
`5ad1659fe3d302021e986b375c63004fbf70406dae88dce80724a0213b73fc39`.
