# RQT-492 — Integral boundary gate
Executed exact local audit against reconstructed RQT-401 Gram, SHA256 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809 (855 exact LLL iterations).
Fix d=1 and z=n=1..9; solve for all integer x per selected integer y using D=(by+cn)^2-a(gy^2+2eyn+fn^2+1). First apply necessary x-existence gates mod 16,9,5,7,11,13,17,19,23,29,31; require D>=0, exact square, and a divides -by-cn±sqrt(D). Test y=-3280..3280 and 3281 consecutive integers outward from each exact real-discriminant boundary. Sign symmetry covers corresponding negative n. 
| n | slices | modular survivors | nonnegative survivors | exact squares |
|---|---:|---:|---:|---:|
|1|13123|5|2|0|
|2|13123|42|25|0|
|3|13123|33|14|0|
|4|13123|0|0|0|
|5|13123|46|27|0|
|6|13123|33|14|0|
|7|13123|25|14|0|
|8|13123|0|0|0|
|9|13123|23|10|0|
Total 118107 slices, 207 modular survivors, 106 nonnegative, zero exact squares. n=4,8 impossible mod16 for all x,y. This is a bounded audit, not a global exclusion. Root19 OPEN; predecessor18 UNVERIFIED. Next: expand boundary-centered search and additional z corridors.
