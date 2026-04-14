// quantum_computer_top.v
// True Quantum Computer — Top-Level Integration
//
// Layers:
//   LAYER 0 (Classical): helical_nand_array    — 8-cell breath, bit-level NAND
//   LAYER 1 (Quantum):   toffoli_helical_gate  — 3-qubit Toffoli, 15-step breath
//
// The two layers share the breath clock but operate independently.
// The Toffoli layer feeds on the CLASSICAL layer's remainder output:
//   • remainder[0] = q0 ancilla seed (T=1 from classical = ancilla=1 for quantum)
//   • data_in[0]   = Signal A (q0 control)
//   • data_in[1]   = Signal B (q1 control)
//
// Mode register:
//   mode=0: CLASSICAL  — helical_nand_array processes data_in[7:0]
//   mode=1: QUANTUM    — toffoli_helical_gate processes q0/q1/ancilla
//   mode=2: DUAL       — both run simultaneously; outputs merged
//
// Conjunction OS interface:
//   Signal A → q0_in (Control)
//   Signal B → q1_in (Control)
//   Classical remainder[0] → q2_in (Ancilla: T=1 preserved from classical layer)
//   Toffoli q2_out → quantum_emergence (∧ in Conjunction OS)
//   Toffoli remainder → quantum_remainder (∇ in Conjunction OS)
//   Toffoli shadow   → quantum_shadow    (⊘ in Conjunction OS)
//
// 0 ≠ 1 | Remainder is signal | CC0 — Saltflower

`include "helical_nand_array.v"
`include "toffoli_helical_gate.v"

module quantum_computer_top (
    input  wire        clk,
    input  wire        rst_n,

    // ── Classical layer interface ────────────────────────────
    input  wire [7:0]  data_in,         // 8-bit input signal
    input  wire        start_breath,    // Trigger classical breath cycle

    // ── Quantum layer interface ──────────────────────────────
    input  wire        start_quantum,   // Trigger Toffoli 15-step breath
    input  wire        ancilla_override, // Override ancilla (1=NAND, 0=AND)
    input  wire        use_override,     // Use ancilla_override instead of classical remainder

    // ── Mode control ─────────────────────────────────────────
    input  wire [1:0]  mode,            // 0=CLASSICAL 1=QUANTUM 2=DUAL

    // ── Classical outputs ────────────────────────────────────
    output wire [7:0]  classical_out,   // Helical NAND result
    output wire [7:0]  classical_rem,   // T=1 remainders from classical layer
    output wire        classical_violation,
    output wire        classical_done,

    // ── Quantum outputs ──────────────────────────────────────
    output wire        quantum_q0,      // Signal A preserved
    output wire        quantum_q1,      // Signal B preserved
    output wire        quantum_emergence, // q2_out = NAND(A,B) or AND(A,B)
    output wire [2:0]  quantum_phase0,  // Phase accumulator A
    output wire [2:0]  quantum_phase1,  // Phase accumulator B
    output wire [2:0]  quantum_phase2,  // Phase accumulator target
    output wire [2:0]  quantum_rem,     // ∇ Toffoli remainder
    output wire [2:0]  quantum_shadow,  // ⊘ Toffoli shadow
    output wire        quantum_inhale,
    output wire        quantum_exhale,
    output wire        quantum_done,
    output wire        quantum_violation,

    // ── Unified Conjunction OS outputs ───────────────────────
    // These are the three-way split in Conjunction OS terms:
    output wire [7:0]  emergence_c,     // Emergence (classical OR quantum)
    output wire [7:0]  remainder_r,     // Remainder ∇ (T=1 preserved)
    output wire [7:0]  shadow_s,        // Shadow ⊘ (phase latent structure)
    output wire        phase_locked     // ∇=0 → clean succession
);

    // ── Ancilla routing ──────────────────────────────────────
    // Quantum layer's ancilla (q2) is seeded by classical remainder[0]
    // This is the constitutional bridge: T=1 from classical becomes
    // the seed qubit for quantum reversibility.
    wire ancilla_in = use_override ? ancilla_override : classical_rem[0];

    // Signal routing: lowest two bits of data_in → qubit controls
    wire sig_a = data_in[0];   // Signal A → q0
    wire sig_b = data_in[1];   // Signal B → q1

    // ── Classical layer: helical_nand_array ──────────────────
    helical_nand_array classical_layer (
        .clk           (clk),
        .rst_n         (rst_n),
        .data_in       (data_in),
        .start_breath  (start_breath),
        .data_out      (classical_out),
        .remainders    (classical_rem),
        .any_violation (classical_violation),
        .breath_complete(classical_done)
    );

    // ── Quantum layer: toffoli_helical_gate ──────────────────
    toffoli_helical_gate quantum_layer (
        .clk           (clk),
        .rst_n         (rst_n),
        .start         (start_quantum && (mode == 2'd1 || mode == 2'd2)),
        .q0_in         (sig_a),
        .q1_in         (sig_b),
        .q2_in         (ancilla_in),
        .q0_out        (quantum_q0),
        .q1_out        (quantum_q1),
        .q2_out        (quantum_emergence),
        .phase0        (quantum_phase0),
        .phase1        (quantum_phase1),
        .phase2        (quantum_phase2),
        .remainder     (quantum_rem),
        .shadow        (quantum_shadow),
        .breath_inhale (quantum_inhale),
        .breath_exhale (quantum_exhale),
        .done          (quantum_done),
        .violation     (quantum_violation)
    );

    // ── Conjunction OS unified output mux ────────────────────
    // Classical mode: direct helical NAND outputs
    // Quantum mode:   Toffoli outputs in Conjunction OS terms
    // Dual mode:      Quantum emergence + classical remainder accumulated
    assign emergence_c = (mode == 2'd1) ?
                             {7'd0, quantum_emergence} :
                         (mode == 2'd2) ?
                             {7'd0, quantum_emergence} ^ (classical_out & 8'h01) :
                             classical_out;

    assign remainder_r = (mode == 2'd1) ?
                             {5'd0, quantum_rem} :
                         (mode == 2'd2) ?
                             {5'd0, quantum_rem} | (classical_rem & 8'h07) :
                             classical_rem;

    assign shadow_s    = (mode == 2'd1) ?
                             {5'd0, quantum_shadow} :
                         (mode == 2'd2) ?
                             {5'd0, quantum_shadow} ^ (classical_rem[7:5] << 5) :
                             {3'd0, classical_rem[7:3]};

    // Phase lock: remainder is zero across both active layers
    assign phase_locked = (mode == 2'd0) ? (classical_rem == 8'd0) :
                          (mode == 2'd1) ? (quantum_rem  == 3'd0)  :
                          (classical_rem == 8'd0) && (quantum_rem == 3'd0);

endmodule
