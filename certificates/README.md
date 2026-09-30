# Exact small-graph certificates

`small_graph_certificates.json` is the exact rational data used for the
32-, 44-, and 72-vertex examples in the paper.  It contains:

- rational Gibbs mixtures;
- nonnegative rational dual multipliers;
- orbit-compressed entries of the rational moment-dual matrix; and
- the positivity margin used only to propose the rounded integer factor.

`theorem_c_context.json` holds the exact data for the Lovász numbers and
fractional packing numbers of the same three graphs, quoted after Theorem C
and checked by `python verify/theorem_c_context.py`. The section "Data format"
below documents both files.

Acceptance does not depend on an SDP solver or a floating-point eigenvalue.
Run `python verify/small_graph_separation.py`.  The script expands every
orbit, checks all affine moment equations in rational arithmetic, and proves
positive semidefiniteness from an integer Gram factor plus an exactly checked
diagonally dominant residual.

The data file was imported byte-for-byte from the jointly maintained research
repository.  Its SHA-256 digest at version 1 is

```text
63119899e5f3bcba30a4121c45c1f95f69020c5bcde7550b610113e678b52058
```

## Data format

This section fixes every convention an independent verifier needs.
`verify/small_graph_separation.py` and `verify/theorem_c_context.py`
implement exactly these conventions.

### Seed graph, vertex order and representation

The nine cells `(i, j)` of the Mermin–Peres magic square (row `i`, column `j`)
carry the two-qubit observables

|       | column 0 | column 1 | column 2 |
|-------|----------|----------|----------|
| row 0 | Z⊗I      | I⊗Z      | Z⊗Z      |
| row 1 | I⊗X      | X⊗I      | X⊗X      |
| row 2 | Z⊗X      | X⊗Z      | Y⊗Y      |

with `Z = diag(1, -1)`, `X = [[0, 1], [1, 0]]`, `Y = [[0, -i], [i, 0]]` and the
standard Kronecker product (first factor = first qubit). The six contexts are
numbered `c = 0, 1, 2` for rows 0, 1, 2 and `c = 3, 4, 5` for columns 0, 1, 2.
The cells of context `c` are taken in the order `(c, 0), (c, 1), (c, 2)` for a
row and `(0, c-3), (1, c-3), (2, c-3)` for a column.

A seed vertex is a context with signs `(s1, s2, s3)` on its three cells, where
`s3 = s1 * s2`, except in context 5 (the last column), where `s3 = -s1 * s2`.
Vertices are numbered context by context,

    v = 4c + p,   p = 0, 1, 2, 3  for  (s1, s2) = (+,+), (+,-), (-,+), (-,-),

so vertex 0 is row 0 with signs `(+,+,+)`. Two distinct vertices are
non-adjacent exactly when they lie in the same context or give opposite signs
to a shared cell (216 ordered non-adjacent pairs). Vertex `v` is represented by
the rank-one projection `Q_v = (I + s1 A1)(I + s2 A2)/4` on C^2 ⊗ C^2, where
`A1`, `A2` are the first two observables of its context; `Q_0 = |00><00|`.

The overlap class of `v` is `j_v = 4 <00|Q_v|00>`, in vertex order

    j = 4 0 0 0 1 1 1 1 1 1 1 1 2 2 0 0 2 2 0 0 2 2 0 0

A `profile` object `{"0": k_0, "1": k_1, "2": k_2, "4": k_4}` defines the clone
graph `F[k]`, in which seed vertex `v` has `k_v = k_{j_v}` pairwise
non-adjacent copies; copies of adjacent seed vertices are adjacent.

### The group A_0

`A_0` is the stabilizer of vertex 0 in the automorphism group of the seed; it
has 48 elements and preserves the overlap classes. The verifiers generate it
(function `symmetries`) as the maps that send a vertex with sign `s` on cell
`(i, j)` to the vertex with sign `f(i, j) * s` on cell `(pi(i), kappa(j))`,
where `pi` fixes row 0 and either fixes or swaps rows 1 and 2, `kappa` is any
permutation of the columns, `f(0, j) = 1`, `f(1, j) = eta_j` with
`eta_1 eta_2 eta_3 = 1`, and `f(2, j) = beta_j beta_kappa(j) eta_j` with
`beta = (1, 1, -1)`. The group acts on monomials letter by letter:
`P_a -> P_g(a)`, `E_b -> E_g(b)`.

### Monomials

The Gram matrix is indexed by 409 monomials, numbered

| index   | vector          | range                                                                               |
|---------|-----------------|-------------------------------------------------------------------------------------|
| 0       | Ω               |                                                                                     |
| 1 + a   | (P_a ⊗ I) Ω     | a = 0, ..., 23                                                                      |
| 25 + b  | (I ⊗ E_b) Ω     | b = 0, ..., 23                                                                      |
| 49–408  | (P_a ⊗ E_b) Ω   | the 360 ordered pairs with a = b or a adjacent to b, in lexicographic order of (a, b) |

so monomial 49 is `(a, b) = (0, 0)` and monomial 408 is `(23, 23)`. Entry
`(i, j)` of the Gram matrix is the moment `m(rev(L_i) L_j, rev(R_i) R_j)`,
where monomial `i` is `(P_{L_i} ⊗ E_{R_i}) Ω` and `rev` reverses a word.
Moments are identified by the rules (R1)–(R4) of Appendix A of the paper, by
reversal of both words, and by `A_0`; this gives 1009 keys. Entries whose
moment vanishes identically by (R1)–(R4) get no key and no equation, and the
corresponding entries of `Z` are restricted only by positivity.

### `small_graph_certificates.json`

`certificates` lists the three graphs in the order G32, G44, G72. Each entry has

- `vertices`: the number of vertices of `F[k]`;
- `profile`: the clone profile, as above;
- `gibbs`: the rational Gibbs witness for the upper bound on `2^C_min`:
  - `states`: a list of `[A, B, w]`. Each item is a magic-square block
    C^2 ⊗ C^2 with center `w * diag(A^4, B^4, B^4, B^4) / (A^4 + 3 B^4)` in the
    basis `|00>, |01>, |10>, |11>`, on which vertex `v` is represented by
    `Q_v`. For a center with eigenvalues `lambda_i` in a basis `|i>`, the Gibbs
    weight of a rank-one `Q` is `prod_i lambda_i^<i|Q|i>`; here it is
    `w * A^(j_v) * B^(4 - j_v) / (A^4 + 3 B^4)`, a rational number. Each
    certificate has one block, with `(A, B) = (41, 56)`, `(56, 51)`, `(3, 4)`.
  - `cliques`: a list of `[C, w_C]`, where `C` is a clique of the seed (seed
    vertices, pairwise adjacent) and `w_C > 0`. Each item is a one-dimensional
    block with center weight `w_C` on which every `v` in `C` is represented by
    `1`; it adds `w_C` to the Gibbs weight of each `v` in `C`. The three
    certificates have 18, 10 and 9 cliques, all of size five.
  - `t`: the exact rational `min over v with k_v > 0 of W_v / (k_v * T)`,
    where `W_v` is the total Gibbs weight of vertex `v` over all blocks and
    `T` is the total weight of the center, the sum of all `w` and `w_C`
    (`T = 999999999/10^9` for G32 and G44, `T = 1` for G72). Dividing by `T`
    normalizes the center, which is legitimate because the weights are
    homogeneous of degree one. This is the certified lower bound on `t_W`, so
    `2^C_min <= 1/t`.
- `harmonic`: the dual certificate for the upper bound on `t_H`:
  - `gamma`: the shift used in the positivity recipe below (`1/100000`,
    `1/5000000`, `1/100000`);
  - `mu`: the 24 multipliers `mu_v >= 0` in seed-vertex order, zero on deleted
    vertices;
  - `Z`: a list of `[i, j, q]` with monomial indices `i, j` and a rational `q`.
    The symmetric 409 × 409 matrix `Z` has `Z[g(i), g(j)] = Z[g(j), g(i)] = q`
    for every listed entry and every `g` in `A_0`, and is zero at every
    position not reached this way. The list holds one representative per orbit
    of `A_0` on positions together with transposition; a file in which two
    listed entries give different values to one position is rejected.

The dual equations: for every key other than the key of `m(∅, ∅)`, the sum of
the entries `Z_ij` at positions with that key, plus the sum of `mu_v` over the
vertices whose harmonic moment `m(∅, v)` has that key, is zero. The number
`lambda` is not stored; it is the same sum at the key of `m(∅, ∅)`. Then
`t_H <= lambda / sum_v mu_v k_v`, so `Sigma >= sum_v mu_v k_v / lambda`.

Positivity recipe. Let `D` be the least common denominator of the entries of
`Z`. Compute a floating-point Cholesky factor `L_f` of the shifted matrix
`Z - gamma I` (not of `Z` itself), require `max |L_f| < 2`, and put
`L = round(2^40 L_f)`, an integer matrix. Check in exact integer arithmetic
that `R = 2^80 D Z - D L L^T` satisfies `R_ii >= sum_{j != i} |R_ij|` for
every row `i`. Then `R` is positive semidefinite, and so is
`Z = L L^T / 2^80 + R / (2^80 D)`. The shift leaves room on the diagonal of
`R` for the rounding error; only the integer check counts.

### `theorem_c_context.json`

`graphs` lists the same three graphs in the same order. A vertex of `F[k]` is
a pair `[x, a]`: seed vertex `x` and copy `a = 0, ..., k_{j_x} - 1`. Each
entry has

- `vertices`, `profile`: as above;
- `independent_set`: a list of pairwise non-adjacent vertices `[x, a]`; its
  size is the claimed Lovász number;
- `theta_dual`: the Lovász dual certificate, with
  - `value`: the claimed Lovász number `a` (an integer);
  - `entries`: a list of `[x, y, same, q]` for seed vertices `x != y` that
    are adjacent in the seed, with `same` always `false` and a rational `q`,
    one entry per orbit of `A_0` on ordered pairs `(x, y)`. The symmetric
    matrix `A` on the vertices of `F[k]` is 1 at every pair
    `[x, c], [y, d]` with `x = y` or with `x`, `y` non-adjacent (these entries
    are not listed), and `q` at every pair of copies of `g(x)` and `g(y)`, for
    every listed `[x, y, false, q]` and every `g` in `A_0`. The verifier
    checks exactly that `a I - A` is positive semidefinite, which by Lovász's
    dual formula gives `theta <= a`; the independent set gives `theta >= a`.
- `packing`: a list of `[x, a, q]`, a fractional vertex packing (unlisted
  vertices get 0) with sum at most 1 on every maximal clique;
- `cover`: a list of `[C, w]`, where `C` is a clique of `F[k]` given as a list
  of vertices `[x, a]` and `w >= 0`, covering every vertex at least once;
- `fractional_packing_number`: the common value of the packing and the cover,
  as a string (`32/5`, `37/4`, `72/5`).
