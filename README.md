# Saltflower

*What grows when you shed your salt?*

A research sketchbook — part theory, part code, part interactive toy. This repo
is a working lab notebook for a single set of ideas about **subtractive
computation, boundary integrity, and emergent coherence**, explored across
writing, simulations, Verilog hardware, and browser demos.

It is deliberately messy. Treat each file as an experiment, not a product.

## Core Philosophy

Everything here orbits a few load-bearing ideas:

- **Stone's Law: 0 ≠ 1**
  A system that admits even one false equivalence (treating unequal states as
  equal) loses integrity. No partial survival.

- **The Breath Cycle (3+1 phases)**
  Inhale novelty → hold / apply torque → exhale / collapse the non-viable →
  return toward zero (without reaching it).

- **T = 1 — the unpaired remainder**
  Coherence is what *survives exclusion*, not what is accumulated. The leftover
  token carries the signal.

- **Helical realm + torque**
  Signals flow with low friction along the axis; torque is paid when misaligned
  states face each other across the radial direction. Ageing = the cumulative
  toll of unavoidable confrontations.

## What's in the box

### Theory & writing
The conceptual spine. Speculative, personal, and a work in progress.

| File | What it is |
|------|------------|
| `theory.md` | "Unification Theory" — the breath cycle, polarity phase-lock, and the Emergent Constitution. The best starting point. |
| `axiom_of_false_equivalence.md` | An information-theoretic essay grounding disinformation detection in conservation of distinguishability (Landauer's principle). |
| `NAND_Attractor_Networks.md` | Subtractive learning via circular NAND topologies that preserve remainder (T=1) signals. Companion study: `NAND_Attractor_Networks_Study.docx`. |
| `Rotational NAND Circuit..md` | Design notes for a "primal math machine" built from helical NAND gates. |
| `Theory of Electomagnetic Coherence.md` | Speculative claim that EM fields act as a universal substrate for living systems. |
| `Universal Theory of Cancer.md` | Reframes cancer as imposed excitation ("thrust") rather than proliferation. |
| `UNIVERSAL_GAME_ENGINE.md` | A blueprint for a polarity-state game engine that replaces 3D geometry with a database of discrete states. |
| `Phase_Engine_Unified_Theory.md.pdf`, `Song_of_the_Stars.docx` | Longer-form documents. |

### The Emergent Laws database
A structured catalog of "emergent laws," each tagged with an evidence level, a
framework role, and admissibility guards.

| File | What it is |
|------|------------|
| `emergent_laws_db.json` | The live database (v9.0, ~163 entries). |
| `emergent_laws_core_v8_2.json` | A curated core subset (~120 entries) focused on materials/math/physics/metaphysics. |
| `emergent_laws_v8_2_changelog.MD` | Notes on the v8.2 restructure (orthogonal `evidence_level` × `framework_role` axes, plus a harm flag). |

### Code & simulation (Python)

| File | What it is |
|------|------------|
| `Math_Machine_v2.py` | A unified-field visualization engine (rotational NAND arrays, Lorentz vortices, spin chains, 3-body, etc.). |
| `remainder.py` | The "3rd phase" — extracts unpaired T=1 tokens and holds them in a carry circuit until they resonate. |
| `quantum_verilog_bridge.py` | Bridges the classical NAND arrays and the quantum Toffoli gate, driving the Verilog FSM and cross-checking it. |

### Hardware (Verilog)
A toy quantum/classical co-processor described in RTL.

| File | What it is |
|------|------------|
| `quantum_computer_top.v` | Top-level module wiring an 8-cell helical NAND array to a 3-qubit Toffoli layer. |
| `toffoli_helical_gate.v` | A 15-gate Toffoli decomposition mapped onto the breath phases. |
| `tb_quantum_computer.v`, `tb_stimulus.vh` | Testbench and stimulus vectors. |

### Interactive demos (open the `.html` files in a browser)
Self-contained toys — no build step.

- **Logic & gates:** `stones_law_visual.html`, `saltflower_gate.html`, `nand_gate_abduction.html`, `the_unbuilt_gate.html`
- **Physics & lattices:** `Accretion Disk Lattice.html`, `hanoi_testbed.html`, `torsed_cable_muscle.html`, `torsed_cable_spec.html`, `Horizon Integrity Theory.html`
- **Sound & soma:** `Muscle OS.html`, `muscle_os_MIDI_bridge.html`, `Saltflower_Chronicle_Trio.html`, `cymatic_signal.html`
- **Visual art:** `pi_pride_mobile.html`, `pi_pride_serotonin.html`, `pride_metal.html`, `Forge Pride.html`, `rayveil.html`
- **Narrative / hubs:** `conjunction_os_v1.0.html`, `heartshard_index.html`
- **Game exports:** `SubtractiveShadersDemo.html` (+ `.pck`)

### Other
- `spacetime` — a SpacetimeDB (Rust) schema for a lattice-navigation game.
- Images: `2=1.png`, `A.png`, `SF4.jpg`, `A History Lesson.jpg`.

## Quick start

Most of the interesting pieces need nothing but a browser — just open any
`.html` file. For the code:

```bash
# The remainder / carry-circuit demo
python remainder.py

# The unified-field visualization engine (needs numpy/matplotlib)
python Math_Machine_v2.py
```

## License & use

The code is **MIT licensed** — see [`LICENSE`](LICENSE). A couple of notes on
the ideas behind it:

- [`ATTRIBUTION.md`](ATTRIBUTION.md) — how to cite, and an ethical-use request.
- [`TRADEMARK_NOTICE.md`](TRADEMARK_NOTICE.md) — which theoretical frameworks are
  trademarked vs. free to use.

By Josh Stone. *For the world, not for money.*
</content>
