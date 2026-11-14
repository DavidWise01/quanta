# RQT-355 — Exact unimodular conic reduction and new finite-height certificate

**2026-11-14. Exact arithmetic executed PASS. Original explicit root18 and roots19–21 remain OPEN.**

## Authentic source
Frozen RQT-242 F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. RQT-351 proves the ternary planes `194/195` and `201/202` rationally isotropic; RQT-353A proves every primitive integer isotropic vector in either has `gcd(F4u)=1`. The present work does not produce an exact integer isotropic witness.

## Constructive integral coordinate reduction

For slope `m/n`, map ternary vector `t=(a,b,c)` to the original integer lattice via
```
T = [[-m,0,0],[0,1,0],[n,0,0],[0,0,1]]
G = T^T F4 T
```
Define an exact 3x3 **unimodular** matrix `V` and new ternary coordinates `z` with `t=Vz`. The reduced Gram is `A=V^T G V`, and `det(V)=-1` for both planes.

```text
194/195:
V = [[1,3,1],[-25,-74,-24],[113,340,113]]
A = [[-561555435662335446,907442644571173949,758956630833872688],
     [907442644571173949,258493091816306268,2583803041170332031],
     [758956630833872688,2583803041170332031,-4624133667290001854]]

201/202:
V = [[1,2,1],[-26,-51,-25],[117,235,117]]
A = [[-932546695834969470,1534419477527031407,793284734389436322],
     [1534419477527031407,-372297003123752932,2700906535086376671],
     [793284734389436322,2700906535086376671,-4184486200006240562]]
```

The maximum absolute Gram-entry decimal length falls from **24 digits to 19 digits** on both planes. The matrices `V` preserve all integer triples bijectively, so these are exact equivalent lattice presentations, not approximations.

## Exhaustive reduced-height exclusion

In each reduced Gram A, the `(z0,z2)` block is **negative definite**. Fix `h=z1`, write the remaining two coordinates as `w=(z0,z2)`, define `P=-A[[0,2],[0,2]]>0`, `v=P^-1 A[[0,2],1]`, and `beta=A11+A[1,[0,2]] P^-1 A[[0,2],1]>0`. Any exact null vector must satisfy
```text
(w-vh)^T P (w-vh) = beta*h².
```
The resulting exact projection bound `(z0-v0h)^2 <= beta h² (P^-1)00` is rounded **outward with exact rational assertions**. Every integer z0 inside the bound is tested. The final z2 coordinate is solved by its integer quadratic discriminant; there is **no artificial limit on z2**.

| slope | positive reduced h | pairs tested | nonnegative discriminants | square discriminants |
|---|---|---:|---:|---:|
| 194/195 | 1..250 | 229,554 | 227,820 | **0** |
| 201/202 | 1..250 | 185,752 | 184,006 | **0** |
| **Total** | | **415,306** | **411,826** | **0** |

For `h=0`, negative definiteness forces the zero vector. By central symmetry, negative h has the same exclusion. Therefore any nonzero primitive integral null vector in either plane must satisfy **`|z1|>=251`**. This is independent of the earlier original-coordinate parameter `|a|>=1001` exclusion, although the two may overlap.

The exact built-in SymPy ternary solver was attempted on the first reduced form but did not finish in the bounded 12-second test. That timeout provides **no mathematical obstruction**. The bounded exact enumeration and the displayed unimodular transforms are the verified results.

## Reproduce and provenance
`python research/rqt355-unimodular-conic-reduction.py` is self-contained, relying on SymPy and Python exact rational/integer arithmetic. The locally executed source is `/mnt/data/rqt355_reduced_search.py` and output `/mnt/data/rqt355_reduced_results.json`. These are computed from one authentic F4 source lineage.

## RQT-356 next natural engineering bound
Use the reduced 19-digit conic with a certified constructive ternary-isotropy algorithm (e.g. arithmetic quaternion splitting, LLL/ideal descent, or a provable quadratic-field norm-equation solver). Alternatively expand exact reduced-height checks with checkpointed evidence. Promote only a genuine integer vector with `u^T F4 u=0` and primitive content, then invoke the RQT-353A divisibility-one theorem and RQT-334 Bézout step. The original explicit roots 18–21 remain OPEN.

The 3×3×3 cubit, Josophene/Juliet and time-angle coordinates remain provenance/indexing metadata, not proof substitutes.
