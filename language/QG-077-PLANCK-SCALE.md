# QG-077 — Planck Scale Bridge

**Carrier:** `{{year,month,day}}[[hour,minute,second]]((degree,arcminute,arcsecond))`. **Natural boundary:** three-bracket temporal-angular address linking the symbolic `{{pb}}` framework (ADA-117A) to measured physics at each power of ten.

## Notation

```
{{year,month,day}}[[hour,minute,second]]((degree,arcminute,arcsecond))
```

Maps to ADA-117A canonical nesting: `{brace,abc[box,bca(torroid,cab)]}`.

| Bracket | ADA-117A | Coordinate | Divisor chain | Total subdivisions |
|---------|----------|------------|---------------|--------------------|
| `{{ }}` | brace | calendar time | 1 year → months → days | ~365.25 days/year |
| `[[ ]]` | box | clock time | 1 day → 24 h → 60 min → 60 s | 86,400 s/day |
| `(( ))` | torroid | angular phase | 1 turn → 360° → 60′ → 60″ | 1,296,000″/turn |

The box and torroid share the same sexagesimal subdivision (QG-025: 60 stations, `60 = 2² × 3 × 5`). The SI second connects them: Earth rotates 15″ of arc per 1 second of clock time.

## The three coordinates and their physics

### {{Brace}} — Calendar time (gravitational)

The year is an orbital period. Earth orbits the Sun at ~1 AU = 1.496×10¹¹ m. This is gravitational mechanics: Kepler's laws, Newton's inverse-square, general relativity at precision. The month has historical lunar origin (~29.53 days synodic). The day is Earth's rotation period.

Scale: 10⁰ m (human) to 10¹¹ m (Earth-Sun). Dominant force: gravity (at macro scale).

### [[Box]] — Clock time (electromagnetic / quantum)

The SI second is defined by the cesium-133 ground-state hyperfine transition: exactly 9,192,631,770 oscillations. This is electromagnetic: the photon frequency of a specific atomic transition at ~3.26 cm wavelength (microwave). The atom that defines the second operates at 10⁻¹⁰ m (atomic scale, electromagnetic force, Coulomb, α ≈ 1/137).

Scale of definition: 10⁻¹⁰ m. Carrier: photon. Force: electromagnetic.

### ((Torroid)) — Angular phase (geometric)

360° × 60′ × 60″ = 1,296,000 arcseconds per turn. This is ADA-116's `TURN` constant (BigInt `1296000n`). Angular phase is geometric, not force-specific — it measures rotation regardless of what causes it.

At astronomical scale: 1 parsec = distance at which 1 AU subtends 1 arcsecond = 3.086×10¹⁶ m. At Planck scale: Planck length / Planck time = c = 2.998×10⁸ m/s (the speed of light itself is a ratio of the two Planck units).

## Physical measurements at each scale

All values are measured or derived from measured constants. Sources in parentheses.

| Power of 10 | What lives here | Measured value | Force regime |
|------------|-----------------|----------------|--------------|
| 10⁻³⁵ m | Planck length | 1.616255×10⁻³⁵ m | quantum gravity (no confirmed theory) |
| 10⁻³⁴ to 10⁻¹⁸ | THE DESERT | no known structure organizes | — |
| 10⁻¹⁸ m | electroweak scale | ~10⁻¹⁸ m (~246 GeV) | electroweak unification |
| 10⁻¹⁵ m | nuclear / QCD | proton radius 0.8414±0.0019 fm (PRad 2019) | strong force, gluons, α_s ≈ 1 |
| 10⁻¹⁰ m | chemistry | C-C bond 1.54 Å, Cs-133 atom | electromagnetic, photons, α ≈ 1/137 |
| 10⁻⁹ m | molecular biology | DNA double helix width ~2 nm | electromagnetic (H-bonds, van der Waals) |
| 10⁻⁶ m | cell biology | typical cell ~10 μm | electromagnetic (biochemistry) |
| 10⁰ m | human scale | ~1.7 m | gravity dominates at macro |
| 10¹¹ m | Earth-Sun | 1 AU = 1.496×10¹¹ m | gravity (Keplerian orbit) |
| 10¹⁶ m | parsec | 1 pc = 3.086×10¹⁶ m | gravity (stellar dynamics) |

**CORRECTION (QG-077):** 10⁻¹⁵ m is NUCLEAR, not chemical. Chemistry organizes at 10⁻¹⁰ m. These are different forces (strong vs electromagnetic), different carriers (gluons vs photons), different coupling constants (α_s ≈ 1 vs α ≈ 1/137), five orders of magnitude apart.

## The bridge

The symbolic `{{pb}}` (ADA-117A) names a structure at the Planck scale. The scale ladder measures what physics finds at each power of 10. The three-bracket notation addresses positions in both frameworks simultaneously.

### What is physical (measured)

- Planck length: ℓ_P = √(ℏG/c³) = 1.616255×10⁻³⁵ m (derived from three measured constants)
- Planck time: t_P = ℓ_P / c = 5.391×10⁻⁴⁴ s
- Proton charge radius: 0.8414 fm (PRad at Jefferson Lab, 2019)
- C-C single bond: 1.54 Å (X-ray crystallography, diamond)
- DNA width: ~2.0 nm (electron microscopy, Watson-Crick B-form)
- SI second: 9,192,631,770 Cs-133 hyperfine oscillations (definition, 1967 CGPM)
- 1 parsec: 3.08567758×10¹⁶ m (defined by 1 AU at 1″ parallax, IAU 2015)
- Speed of light: c = 299,792,458 m/s (defined, SI 2019)
- Wheeler foam (1955 picture): simplest versions observationally dead per Fermi LAT (GRB 090510, 2009) and MAGIC telescope constraints

### What is symbolic (ADA-117A)

- `{{pb}}` = Planck bubble / Lead-208 anchor
- 208 = symbolic numerical anchor, not a physical identification with a Planck bubble
- Cyclic permutation abc → bca → cab = three orientations of one structure
- Event admission is forward-only in an append-only ledger (ADA-117B `admit()`)
- One simulated communication round = one angular arcsecond of model phase (ADA-116)
- No physical equivalence between angle and Planck time is asserted

### The composite address

A full address in the notation:

```
{{2026,11,17}}[[14,30,00]]((127,23,45))
```

reads: calendar 2026 November 17, clock 14:30:00, angular phase 127°23′45″.

The three brackets are independent coordinates. Calendar time does not convert to angular phase. Clock time does not convert to calendar time (except through the physical fact that Earth rotates once per day). The notation holds all three without asserting equivalence.

The scale ladder positions tag WHERE on the physical ruler a symbolic event is anchored. The `{{pb}}` primitive addresses Planck-scale (10⁻³⁵ m). The cesium atom that defines the SI second operates at atomic scale (10⁻¹⁰ m). The year that marks calendar time comes from orbital mechanics at solar-system scale (10¹¹ m). Three scales, three forces, three brackets.

## Observational constraints

The simplest spacetime foam models predict energy-dependent photon dispersion: Δt ∝ E/E_Planck × d/c. Fermi LAT observation of GRB 090510 (2009) and MAGIC telescope observations constrain this to below the Planck scale for linear models, ruling out the simplest Wheeler foam pictures. The scale exists (dimensional analysis demands it); the foam probably doesn't.

The holographic principle (black hole entropy ∝ horizon area, not volume: Bekenstein 1973, Hawking 1975) constrains what Planck-scale structure can look like — information density at the boundary, not in the bulk.

## Test targets

1. All three bracket types parse independently.
2. Clock subdivisions: 24 × 60 × 60 = 86,400.
3. Angular subdivisions: 360 × 60 × 60 = 1,296,000 = ADA-116 TURN.
4. Earth rotation bridge: 15 arcseconds of arc per 1 second of clock time (360° / 86400 s × 3600″/° = 15″/s).
5. Scale assignments verified against published measurements.
6. Physical values carry uncertainty; symbolic values are exact integers.
7. No physical equivalence between bracket types is computed or inferred.

## Sources

- CODATA 2018 Planck length: NIST SP 961 (2019)
- PRad proton radius: Xiong et al., Nature 575, 147–150 (2019)
- Fermi LAT GRB constraint: Abdo et al., Nature 462, 331–334 (2009)
- Bekenstein-Hawking entropy: Bekenstein, Phys. Rev. D 7, 2333 (1973); Hawking, Commun. Math. Phys. 43, 199 (1975)
- IAU 2015 parsec definition: IAU Resolution B2 (2015)
- SI second (Cs-133): 13th CGPM Resolution 1 (1967)
- SI 2019 (fixed c): 26th CGPM Resolution 1 (2018)

## Ancestry

- [ADA-117A diodic-pb](../ada/living-116/diodic-pb-117a.md) — symbolic `{{pb}}` primitive
- [ADA-116 arcsecond continuity](../ada/living-116/index.html) — TURN = 1,296,000
- [ADA-117B diodic PB viewer](../ada/living-117b/index.html) — 208 symbolic anchor, integer phase clock
- [QG-025 sexagesimal 60](./QG-025-SEXAGESIMAL-60.md) — the 60-ring that generates both minute and arcsecond
- [QG-050 ambiguous roots](./QG-050-AMBIGUOUS-ROOTS.md) — observer must preserve candidates
- [planck-scale-ladder.html](../planck-scale-ladder.html) — physical measurement instrument

## Artifacts

- [Bridge instrument](../planck-scale-bridge.html)
- [Scale ladder](../planck-scale-ladder.html)
