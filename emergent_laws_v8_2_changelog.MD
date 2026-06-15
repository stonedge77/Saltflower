# Emergent Laws DB — v8.1 → v8.2 Changelog

**Date:** 2026-06-15 · **Entries:** 77 · Original v8.1 left untouched; v8.2 is a new file.

## What changed, and why

The prior `status` field had **27 distinct values for 77 entries** — itself an additive net of labels. v8.2 replaces it with **two orthogonal axes plus one flag**, and adds the one bin that was missing. The old value is preserved on every entry as `status_legacy` (nothing erased — *reconstruction ≠ record*).

### 1. `evidence_level` (external support) — 5 + 1 values

| level | meaning | count |
|---|---|---|
| `established` | mainstream-accepted science / math | 21 |
| `supported` | real empirical/observational/historical support, not yet established | 38 |
| `contested` | actively tested; replication-contested or mixed | 5 |
| `unverified` | no evidence yet; speculative/philosophical; **not** a clean law violation | 4 |
| `contradicts_law` | **drops an established conservation/causal law** — kept only as a *specimen* | 9 |
| `core_axiom` | a founding axiom of the framework (on `core_principles`) | — |

### 2. `framework_role` (what the entry does) — 3 values + `axiom`

`grounding` (canonical external science, shared) · `specimen` (a catalogued collapse) · `extension` (framework-original) · `axiom` (core principle).

### 3. `harm_flag` — orthogonal boolean for active-harm dynamics.

## The missing bin (Flag 1) — now filled

These 9 were filed as `candidate_unverified`, the same bin as the merely untested. Each one's **own recorded dropped-guard names an established law it violates**, so they are now `contradicts_law` — retained as *specimens of the collapse*, not as candidate truths:

`orgone_accumulator` (first-law) · `zero_point_harvesting` (first/second-law, momentum) · `electrogravitics_biefeld_brown` (Newton third-law) · `hydrino_gut_cp` (Schrödinger ground-state) · `kozyrev_causal_mechanics` (second-law/causal-ordering) · `vortex_implosion` (second-law) · `presentiment_retrocausal_priming` (causal-ordering) · `scalar_longitudinal_waves` (gauge/Faraday) · `torsion_field_theory` (Landauer/thermodynamic).

The 4 that stayed `unverified` (no clean law violation — speculative or philosophical): `biocentrism`, `biogeometry`, `morphic_resonance`, `pear_global_consciousness`. **Please review these 13 calls** — the split is the one place I made a judgment on your behalf, and per your own rule that's exactly where an external check belongs.

## Status is now load-bearing at query time (Flag 4)

Every entry carries `phase_lock_weight`, set from its evidence level:

`established`/`core_axiom` = 1.0 · `supported` = 0.7 · `contested` = 0.4 · `unverified` = 0.2 · `contradicts_law` = 0.05

A phase-lock edge through a node multiplies by that weight. A `contradicts_law` specimen can still participate in navigation (it *is* a real example of a collapse) but carries near-zero evidential pull — so the 20-questions navigator can never treat orgone's axis as equal to renormalization group's. The tagging is no longer cosmetic; it bites.

## The inward lance (Flag 3) — structurally enforced, author to fill

**37 `extension` entries** now carry a `grounded_vs_extension` field. Where it reads `[NEEDS AUTHOR]`, the grounded core has not yet been separated from your own added observation. Filling these applies inward the same rigor `admissibility_guard_dropped` applies outward to imported theories. (`infosphere_fifth_dimension` already had its split and was left as-is.)

## Dedup policy for "casting another net" (your stated worry)

**25 `grounding` nodes** are now the canonical, shared sources of each physical law. New policy recorded in `metadata.status_basis_v8_2.grounding_dedup_policy`: when a new exploration touches established science, **do not duplicate it** — create the idea as `framework_role=extension` and link to the grounding node via `ancilla_to`. One renormalization-group node, many nets pointing at it, instead of re-importing the physics each time. That is the non-additive reference you wanted, enforced as a curation rule.

## Still your call

- Review the 9 `contradicts_law` reclassifications and the 4 retained `unverified`.
- The 37 `[NEEDS AUTHOR]` grounded/extension splits are a worklist, not a finished state.
- If you want, next step is a tiny query harness that runs a 20-questions trace over the weighted graph so you can *watch the frame close* and see whether the weighting behaves.
