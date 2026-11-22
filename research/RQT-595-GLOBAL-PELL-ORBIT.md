# RQT-595 — Global Pell Orbit Reconstruction: family 28

## Exact target
RQT-583 surviving selected family index **28**, ray `[45,-13,18]`, offset `[-1,-1,0]`. The original archived Pell JSON SHA-256 is `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`. Using the exact RQT-591 rederived 4×4 Gram:
```
A = 89518360633605555683821304281344825
B = -7483520243911231029085168265101895934
C = -64071240985594466694007969119178624871
D = 78945285068193588880454794453306132157010594392916809771448116369654302656
N = 4A = 358073442534422222735285217125379300
```
The generalized Pell form `X²-NY²=D`, `X=2At+B`, `Y²=At²+Bt+C`, is verified exactly at signed t values against the rederived Gram discriminant.

## Pell unit and orbit gates
An exact continued-fraction recurrence for `sqrt(N)` checked its first **10,000** convergents. **No convergent was a norm +1 unit**. This is a bounded computation, not a theorem ruling out a fundamental unit.

Constructed a nontrivial rational norm-one transformation:
```
p = floor(sqrt N) = 598392381748315895
U = p²+N = 716146885068844444593653885835030325
V = 2p = 1196784763496631790
W = p²-N = -876916548415728275
U² - N V² = W²
X' = (U X + N V Y)/W
Y' = (V X + U Y)/W
```
The transform preserves the Pell norm **over Q** exactly. It is **not certified as an integral orbit action**: to preserve integer coordinates requires divisibility of both numerators by W, and `X' ≡ B (mod 2A)` to recover integer t. Any resulting square-root sign must recover integral u and the full norm −2. No seed of the generalized Pell equation has yet been certified.

The exact finite search for `−12000 ≤ t ≤ 12000` on family 28 found zero square discriminants and zero recovered integer pairs. A finite nonfinding is not an all-scale exclusion.

## Status
Selected corridor ledger **82 excluded / 53 unresolved** out of 135. No new exclusions. 22-dimensional Wall replay NOT performed. Root19 OPEN.

## Next natural bound — RQT-596
Do not repeat unbounded convergent scanning. Prove the orbit integrality gate for an explicit rational-unit iterate or find a genuine norm-one integral unit and a generalized Pell seed; then enforce `X ≡ B (mod 2A)` and integral u before any original 22D Wall claim.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
