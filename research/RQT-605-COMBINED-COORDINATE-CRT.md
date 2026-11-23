# RQT-605 — Combined Coordinate CRT & Exact Norm Gate

## Inputs and replay

Reopened the RQT-604 chain of 53 family certificates and the RQT-591 rederived 4×4 Gram. Verified source Gram SHA-256 `f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228` and the RQT-604 chain tip `e2bd1c5818a294ecd578af40791c81b3b96c432ee9276f0f404b7e4b054994a2`. Every family-record hash was recomputed from canonical JSON and its previous-record hash validated.

## Combined exact coordinate congruences

Selected the pairwise coprime moduli:

```
256,81,125,49,11,13,17,19,23,29,31
M = 121298984430624000
```

For each family, recovered the previously verified example coordinate pairs `(u_i,t_i)` for every modulus `m_i`. Applied CRT independently to the u and t coordinates:

```
u ≡ u_i (mod m_i)
t ≡ t_i (mod m_i)
```

The combined representative was checked against the original rederived 4×4 Gram through `q_F((u,ray*t+offset))+2`. It vanished modulo every component modulus and hence modulo M. All **53/53** families passed.

Moreover, the total number of admissible coordinate pairs modulo M equals the **product** of the per-modulus counts, by the CRT bijection `(Z/MZ)^2 ≅ Π_i (Z/m_i Z)^2`; a positive count is not an integer root.

This does not newly exclude any family: simultaneous solvability for coprime coordinate congruences follows from CRT, and the computed witnesses give concrete reproducible confirmation for this particular ledger. No 22D Wall replay was performed.

## Exact scope / status

- 53 combined family witnesses.
- 11 pairwise coprime modular factors.
- Exact combined modulus: **121298984430624000**.
- All 53 norm congruences pass modulo M.
- New all-scale exclusions: **0**.
- Selected family ledger: **82/135 excluded (60.74%); 53 unresolved**.
- Selected corridors do not exhaust the entire rank-four lattice.
- Root19 **OPEN**.

## Next bound — RQT-606

Use the verified combined CRT classes to test **lifting toward exact integer solutions**, with bounded distance-to-zero and exact norm evaluation. Prioritize constructing a genuine `q_F=-2` candidate; do not interpret a modular zero as a global integer zero. If the direct approach fails within a finite budget, preserve a nonfinding certificate and investigate structural conditions beyond local congruences.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
