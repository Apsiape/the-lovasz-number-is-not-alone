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
