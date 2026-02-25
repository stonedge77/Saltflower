Cyclic Remainder-Preserving NAND: A Phase-Rotated Universal Logic Primitive
Abstract
We present a novel logic primitive — Cyclic NAND — that reframes the classical NAND gate as a phase-rotated, lossless computational unit. Where conventional NAND operations are irreversible and information-destroying (Landauer, 1961), Cyclic NAND preserves a one-bit parity remainder at each operation cycle, enforcing strict bit-level distinction (0 ≠ 1) as an architectural invariant. Eight cells arranged in a closed feedback ring each apply π/4 phase increments, completing a full 2π rotation per logical cycle. The architecture achieves universality over classical Boolean logic, maps cleanly to reversible gate primitives (Toffoli/CCNOT), and offers native parity checking, thermal distribution through recirculation, and fault rerouting. We propose this as a substrate for low-power, remainder-preserving computation.

1. Introduction
The NAND gate is a classical universal primitive: any Boolean function can be expressed entirely in NAND. However, standard NAND implementations are logically irreversible — input states cannot be recovered from output states alone — incurring a theoretical minimum energy cost of kT ln 2 per bit erasure (Landauer's principle). Reversible computing frameworks (Bennett, 1973; Toffoli, 1980) address this by constructing information-preserving circuits from gates such as CCNOT (Toffoli) and CSWAP (Fredkin), eliminating erasure overhead entirely. These approaches, however, treat remainder bits as ancillae to be reset, rather than as structurally meaningful outputs.
We propose a different framing: rather than treating the remainder as overhead, make remainder preservation an architectural constraint. Cyclic NAND enforces this by routing each operation's carry/parity bit back into the computation loop rather than discarding it.

2. Architecture
The core unit is a ring of eight NAND cells. Each cell executes the following four-phase subcycle:

Input latch — capture operands
Phase rotation — apply a π/4 phase shift to the signal representation (interpretable as a rotation in the complex plane or as a delay element in a clocked system)
NAND evaluation — compute output
Remainder recirculation — route the XOR of input and output (the parity remainder, T = A XOR B XOR NAND(A,B)) back into the ring head

After eight cells, the ring has accumulated a full 2π phase rotation and the recirculated remainder stream constitutes a running parity register over the entire computation history. No bit is discarded.
This is structurally analogous to a linear feedback shift register (LFSR) with a NAND-based feedback polynomial, but with the additional constraint that each tap preserves rather than overwrites prior state.

3. Remainder Preservation
At each cell, define the remainder bit as:

T = A ⊕ B ⊕ NAND(A, B)

This is the residue that a standard NAND gate discards. In Cyclic NAND, T is recirculated as an input modifier to the next cell. After a full eight-cell cycle, the cumulative remainder encodes the parity of all operations in that pass — functioning as a native, zero-overhead error detection register.
This is distinct from standard parity-check augmentation (where parity is computed separately and appended) because the remainder is intrinsic to the computation path rather than a parallel check circuit.

4. Universality
Classical: Any Boolean function expressible in standard NAND can be implemented in Cyclic NAND with at most a constant overhead factor determined by remainder routing. The NAND-completeness proof carries over directly since each cell still computes NAND(A,B); the recirculation path does not alter the primary output.
Reversible: Cyclic NAND embeds into the Toffoli gate (CCNOT) via the standard 15-gate decomposition using T and T† (π/4 rotation) gates from the Clifford+T gate set. The π/4 per-cell phase structure of Cyclic NAND maps directly onto T-gate depth in this decomposition, making the translation natural rather than ad hoc.
Quantum: The π/4 phase rotation per cell corresponds to the T gate in the standard quantum gate set {H, CNOT, T}. A full eight-cell cycle corresponds to a T⁸ = I rotation (identity up to global phase), with intermediate states spanning the non-Clifford portion of the Bloch sphere. This suggests a potential mapping to fault-tolerant quantum computation via magic state distillation.

5. Fault Tolerance and Thermal Properties
Because computation is distributed across eight cells in a closed ring rather than a linear feed-forward chain, single-cell failure can be detected via remainder discontinuity (a dropped or corrupted T bit breaks the parity invariant) and rerouted by bypassing the failed cell and compensating with an adjusted phase offset in subsequent cells.
Heat dissipation is similarly distributed: since no operation irreversibly erases a bit, the Landauer lower bound is not triggered at any single cell, and thermal load is spread across the ring. In the reversible limit, total heat generation approaches zero; in a physical implementation with leakage, the ring structure ensures no single cell bears disproportionate thermal burden.

6. Discussion
The key departure from prior work is the treatment of the remainder not as an ancilla to be reset (as in standard reversible computing) but as a first-class signal that carries semantic content — specifically, the running parity of the computation. This has precedent in carry-save arithmetic and residue number systems, but has not, to our knowledge, been applied at the level of the universal gate primitive itself.
Open questions include: the minimum ring size required to guarantee remainder integrity across arbitrary Boolean functions; the overhead cost (in gate count and latency) of remainder routing in large circuits; and whether the T-gate correspondence enables direct compilation of Cyclic NAND circuits to fault-tolerant quantum hardware.

7. Conclusion
Cyclic NAND extends the classical universal NAND primitive with remainder preservation, phase-rotation structure, and closed-loop recirculation. It achieves universality over Boolean logic, maps naturally to reversible and quantum gate sets, and provides native parity checking and fault detection as intrinsic properties rather than add-on circuits. We propose it as a foundational primitive for architectures where information preservation, thermal efficiency, and structural error detection are first-order design constraints.
