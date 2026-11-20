# RQT-522 — Batched Norm Sieve

Conditional frozen Gram SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`. Predecessor root18 **UNVERIFIED**; root19 **OPEN**.

Algorithm: for the conditional d=1 form `t² + A k² = E(x)=Jx²−Af`, generate primes p in [1500000,20000000), retaining those satisfying Legendre(-A,p)=-1. Multiply up to 256 consecutive qualifying primes per batch P, compute g=gcd(E,P) for each still-unresolved corridor; if g>1, isolate p and certify odd valuation. An odd valuation at an inert prime is an exact necessary-condition obstruction for the entire fixed-x corridor.

**Executed:** 578,729 qualifying inert primes, 2,261 batches, runtime 23.398s. Five new fixed-x exclusions with valuation 1:

| Prior RQT-521 index | p | v_p(E) |
|---:|---:|---:|
|36|2038451|1|
|23|5061677|1|
|94|6705359|1|
|104|6725497|1|
|88|7456327|1|

Selected 720-corridor ledger: **630 excluded, 90 unresolved**. Sum of remaining complete y-interval widths: `52981813352036635192`. The surviving norm equations were not fully factored or solved, and no exact integral root was found. No global nonexistence result is claimed. Seven-level sexagesimal geometry remains navigation context, not exhaustive angular enumeration.

Exact local engine and full JSON are in the associated conversation artifacts; the GitHub HTML below is a text research viewer. A separate locally generated embedded-JPG HTML chronicle also exists.

**Next RQT-523:** factor-aware constructive norm representation and exact t,k→y,z back-mapping.
