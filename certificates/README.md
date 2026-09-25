# Exact small-graph certificates

`small_graph_certificates.json` is the exact rational data used for the
32-, 44-, and 72-vertex examples in the paper.  It contains:

- rational Gibbs mixtures;
- nonnegative rational dual multipliers;
- orbit-compressed entries of the rational moment-dual matrix; and
- the positivity margin used only to propose the rounded integer factor.

Acceptance does not depend on an SDP solver or a floating-point eigenvalue.
Run `python verify/small_graph_separation.py`.  The script expands every
orbit, checks all affine moment equations in rational arithmetic, and proves
positive semidefiniteness from an integer Gram factor plus an exactly checked
diagonally dominant residual.

The data file was imported byte-for-byte from the jointly maintained research
repository.  Its SHA-256 digest at version 1 is

```text
0ed543d81d5a14d569ac5711f534ced19ca3e1a910d91c606f48e53a66075f7a
```
