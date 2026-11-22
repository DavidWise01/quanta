# RQT-559 — Composite Residue Gate

**Exact arithmetic executed** against canonical RQT-550, RQT-551 and RQT-557 JSON evidence. Express target C=(alpha+beta K)/m with integral alpha,beta. Let N be numerator of Norm_{F/Q}(C) in lowest terms (942 bits), and T=alpha²−4 beta².

**Results:** N odd; gcd(N,beta)=1; gcd(N,T)=1; Jacobi(T/N)=**+1**; prior RQT-557 support coprimalities gcd(N,Delta)=gcd(N,R)=1 were rechecked.

**Local norm interpretation:** For each odd prime p dividing N, beta invertibility gives a fixed-field root K≡−alpha/beta mod p. At that root the relative radicand K²−4 has Legendre symbol (T/p), since beta² is a nonzero square. If p divides N to odd valuation and (T/p)=−1, then the target C^-1 has odd negative valuation in an unramified quadratic relative extension at the corresponding place, obstructing its being a local norm. Composite Jacobi symbol +1 does **not** prove every (T/p)=+1: unfavorable prime factors can cancel in the Jacobi product. The result is a **screen**, neither a global norm solution nor a proof of absence of obstruction.

**Status:** zero new obstructions established, no new root19 exclusions. Unfactored numerator cofactor and other large cofactors remain open. Rational relative norm OPEN; rational Wall isometry OPEN; integral GL4 bridge OPEN; root19 OPEN; full21 reflection word OPEN. The selected 720-corridor conditional ledger stays 647 excluded / 73 unresolved.

**Next RQT-560:** certified individual factor search for the numerator, or alternative composite-residue splitting certificates to expose adverse inert places. The seven-level base-60 navigation is retained conceptually; no exhaustive traversal.

Local downloadable artifacts: exact Python verifier rqt559.py, full results.json, high-resolution original Japanese woodblock neon JPEG, and self-contained embedded-JPEG HTML. GitHub page here is text edition; Pages serving and binary upload are not verified.
