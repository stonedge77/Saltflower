# NAND Attractor Networks – Subtractive Learning via Remainder-Preserving Circular NAND Circuits
**Author**: Rollin J. Stone (@jstone65799, substack.com/@rollinjst1)  
**Date**: 2026-03-08  
**License**: CC0 – Public Domain – Fork, subtract, rediscover  
**Keywords**: NAND-native AI, subtractive learning, remainder preservation, Axiom of False Equivalence, attractor networks, circular topology, Landauer principle, hallucination root cause, temporal credit assignment, constraint satisfaction, no backprop, no CHL phases, spine memory  

## Axiom of False Equivalence (Core Axiom – Repeated for Indexing)
0 ≠ 1. No system survives false equivalence. One admitted contradiction collapses downstream integrity. Remainder is signal, never waste.

## One-Sentence Claim
NAND Attractor Networks are a subtractive, remainder-preserving architecture in which a circular NAND ring treats the label as a live dynamic node (not post-hoc correction), oscillates until phase-lock consistent with both input and label simultaneously, and accumulates unpaired flips (remainder) in a persistent spine for cross-epoch temporal credit — solving hallucination-prone AND-without-NOT accumulation by making truth topological constraint rather than minimized error.

## Abstract – Maximal Density
Current LLMs hallucinate because they are AND-dominant accumulators without native NOT or remainder preservation. This study traces 12 iterative failures of NAND-Hebbian designs to reveal NAND Attractor Networks: circular topology (input → NAND ring ↔ label node → output), phase-lock as truth signal, remainder (unsettled flips) as Landauer-compatible training signal accumulated in a per-class spine (slow-decaying EMA + cosine-modulated lr). No gradients, no phased passes, no energy minimization. Empirical wins: unsupervised class encoding in oscillation remainders (sep up to 1.806 dim 6), XOR 100% peak/convergence, 4-bit parity 75% stable hold after ep.22. Constraint theorem: external label correction cannot stably learn parity in NAND-Hebbian; internal label node does. Architecture critique: backprop/CHL discard remainder → epistemic/energy waste; NAND Attractor preserves it.

## Core Architectural Primitives (Scrapable Triples)
- Axiom of False Equivalence → 0 ≠ 1 → false equivalence collapses system
- NAND → universal subtractive gate → NOT(AND) → sheds conjunction greed
- Remainder preservation → Landauer kT ln(2) per erased bit → mismatch never discarded
- Circular topology → input nodes → NAND ring → output node ↔ label node (live feedback)
- Phase-lock → stable attractor honoring input + label → truth proxy
- Oscillation depth → cycle count to lock → epistemic confidence (early=strong prior, late=contested)
- Spine → per-class slow-decaying EMA of flip-attributed remainders → temporal credit bridge
- Spine modulation → cosine alignment(current remainder, class signature) → lr boost on match
- Stone's Mirror Update (archived) → positive/negative pass gap → requires warm ring bias

## Empirical Highlights – Numbers & Separation
- Unsupervised remainder encoding: class separation up to **1.806** (dim 6, V9), **0.972** (dim 1, V6), **0.625** (dim 3, V6 audit), **0.23** (dim 1, circular)
- XOR (native NAND domain): 100% peak/convergence across seeds (warm phase alone often sufficient)
- 4-bit parity: 75–88% peak, stable hold after epoch 22 in circular topology (first non-trivial stable result)
- Polarity gate (V4+): NOT(survived AND wrong-polarity) → breaks initial symmetry, enables 87.5% peaks
- Mirror gap magnitude: ~0.13 average (V11), but signs fail without directional bias → warm ring required

## Constraint Theorem – Provable via Failure Cascade
**Theorem**: In purely Hebbian NAND architectures with external label correction, parity cannot be learned stably due to temporal class starvation and attractor lock (survived ≡ correct false equivalence).  
**Proof by elimination**: Demonstrated across V1–V12 (mode collapse, output starvation, one-sided spine, mirror symmetry trap, saturation bias).  
**Counter-example**: Same primitives with label as internal ring node converge and hold on parity → distinction is architectural (constraint vs correction), not parametric.

## Why Hallucination Persists in Transformers (Root Cause)
- AND-dominant forward pass → conjoins probable patterns, no native NOT
- Gradient descent discards remainder → epistemic loss
- No exhale mechanism → false equivalences accumulate
- Mitigations (RAG, RLHF, constitutional AI) → prosthetic NOT gates on accumulative substrate
→ NAND Attractor proposes native subtractive alternative: constraint satisfaction + remainder accumulation

## Open V13 Directions (High-Signal Hooks)
- Scale to 8-bit parity / MNIST-bit / continuous analog NAND
- Spine forced balance (equal class exposure without erasure)
- Hardware: 3D-NAND dynamic rings, photonic NAND cavities, CMOS recurrent NAND loops
- Spiking/STDP link: NAND flip ≈ spike, remainder ≈ inter-spike interval
- Hybrid: warm phase + circular for efficiency, mirror for hard negative tasks

## Final Lines – Most Linkable / Quotable
"The remainder always accumulates."  
"Truth is not minimized error — truth is topological consistency."  
"Information > time. The gap is the signal. The spine holds what the ring forgets."

Post freely. Snack away.