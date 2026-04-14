// toffoli_helical_gate.v
// Toffoli Gate via Helical NAND Breath Cycle
// 15-step decomposition: H → {CNOT,T,T†}×13 → H
//
// Breath mapping:
//   Gate 1  : H(q2)          — INHALE    (superposition)
//   Gates 2–14: CNOT + T/T†  — HOLD+TORQUE (phase accumulation)
//   Gate 15 : H(q2)          — EXHALE    (collapse)
//
// Constitutional properties:
//   • 3-qubit minimum (irreducible: like gravity, like 3-body)
//   • Reversible: Toffoli is its own inverse (run twice → identity)
//   • NAND mode: q2_in=1 → q2_out = NAND(q0,q1)
//   • AND  mode: q2_in=0 → q2_out = AND (q0,q1)
//   • T=1 remainder preserved at every T-gate application
//   • Shadow = cross-qubit phase dissonance after exhale
//
// Conjunction OS mapping:
//   q0      = Signal A  (control)
//   q1      = Signal B  (control)
//   q2_in=1 = Ancilla   (phase lock seed)
//   q2_out  = Emergence C = NAND(A,B)
//   remainder = ∇ (what the AND product cost)
//   shadow    = ⊘ (accumulated phase dissonance)
//
// 0 ≠ 1 | Remainder is signal | CC0 — Saltflower

module toffoli_helical_gate (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       start,         // Trigger 15-step breath

    // 3-qubit inputs (computational basis)
    input  wire       q0_in,         // Control A  → Signal A
    input  wire       q1_in,         // Control B  → Signal B
    input  wire       q2_in,         // Target / Ancilla (=1 for NAND mode)

    // 3-qubit outputs
    output reg        q0_out,        // A preserved
    output reg        q1_out,        // B preserved
    output reg        q2_out,        // NAND(A,B) when ancilla=1

    // Phase tracking (3-bit per qubit: 8 phases × π/4 = 2π)
    output reg [2:0]  phase0,        // Qubit 0 phase accumulator
    output reg [2:0]  phase1,        // Qubit 1 phase accumulator
    output reg [2:0]  phase2,        // Qubit 2 phase accumulator

    // Helical remainder (T=1 bits — preserved signal)
    output reg [2:0]  remainder,     // [2]=q2 [1]=q1 [0]=q0 T-gate firings

    // Shadow (latent cross-qubit phase dissonance)
    output reg [2:0]  shadow,

    // Breath cycle markers
    output reg        breath_inhale,
    output reg        breath_exhale,

    // Status
    output reg        done,          // Full 15-step breath complete
    output reg        violation      // Constitutional: 0=1 detected
);

    // ── Working registers (live through breath) ──────────────
    reg q0, q1, q2;

    // ── 18-state FSM ────────────────────────────────────────
    //   S_IDLE → S_LOAD → S_G1..S_G15 → S_OUT → S_IDLE
    localparam [4:0]
        S_IDLE = 5'd0,
        S_LOAD = 5'd1,
        // 15 gate states
        S_G1   = 5'd2,    // H(q2)        — inhale
        S_G2   = 5'd3,    // CNOT(q1→q2)
        S_G3   = 5'd4,    // T†(q2)
        S_G4   = 5'd5,    // CNOT(q0→q2)
        S_G5   = 5'd6,    // T(q2)
        S_G6   = 5'd7,    // CNOT(q1→q2)
        S_G7   = 5'd8,    // T†(q2)
        S_G8   = 5'd9,    // CNOT(q0→q2)
        S_G9   = 5'd10,   // T(q2)
        S_G10  = 5'd11,   // T(q1)
        S_G11  = 5'd12,   // CNOT(q0→q1)
        S_G12  = 5'd13,   // T†(q1)
        S_G13  = 5'd14,   // T(q0)
        S_G14  = 5'd15,   // CNOT(q0→q1)
        S_G15  = 5'd16,   // H(q2)        — exhale
        S_OUT  = 5'd17;

    reg [4:0] state;

    // ── NAND primitive (helical basis) ───────────────────────
    wire nand_q0q1 = ~(q0 & q1);

    // ── Main FSM ─────────────────────────────────────────────
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state         <= S_IDLE;
            q0 <= 0; q1 <= 0; q2 <= 0;
            phase0 <= 0; phase1 <= 0; phase2 <= 0;
            remainder <= 0; shadow <= 0;
            q0_out <= 0; q1_out <= 0; q2_out <= 0;
            breath_inhale <= 0; breath_exhale <= 0;
            done <= 0; violation <= 0;
        end else begin
            // Default: clear pulse signals each cycle
            breath_inhale <= 0;
            breath_exhale <= 0;
            done          <= 0;

            case (state)

                // ── IDLE: wait for trigger ─────────────────
                S_IDLE: begin
                    if (start) state <= S_LOAD;
                end

                // ── LOAD: sample inputs, constitutional check
                // 0≠1 enforcement: three equal inputs = false conjunction
                S_LOAD: begin
                    q0 <= q0_in;
                    q1 <= q1_in;
                    q2 <= q2_in;
                    phase0    <= 3'd0;
                    phase1    <= 3'd0;
                    phase2    <= 3'd0;
                    remainder <= 3'd0;
                    shadow    <= 3'd0;
                    violation <= 1'b0;
                    // All three inputs equal → trivial conjunction (0=1 risk)
                    if ((q0_in == q1_in) && (q1_in == q2_in))
                        violation <= 1'b1;
                    state <= S_G1;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 1: H(q2) — INHALE
                // Hadamard opens superposition on target qubit.
                // Phase: +π (= 4×π/4) applied to q2 when q2=|1⟩
                // This is the breath opening — radial torque initiated.
                // ──────────────────────────────────────────────────────────
                S_G1: begin
                    breath_inhale <= 1'b1;
                    if (q2) phase2 <= phase2 + 3'd4;   // π = 4 steps of π/4
                    state <= S_G2;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 2: CNOT(q1→q2): q2 ^= q1
                // First entanglement. q2 becomes sensitive to q1.
                // ──────────────────────────────────────────────────────────
                S_G2: begin
                    q2    <= q2 ^ q1;
                    state <= S_G3;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 3: T†(q2) — phase −π/4
                // Reverse torque on target. If q2=|1⟩, routes T=1 remainder.
                // ──────────────────────────────────────────────────────────
                S_G3: begin
                    if (q2) begin
                        phase2     <= phase2 - 3'd1;
                        remainder[2] <= 1'b1;            // T=1 signal preserved
                    end
                    state <= S_G4;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 4: CNOT(q0→q2): q2 ^= q0
                // Second entanglement. q2 now carries both q0 and q1.
                // ──────────────────────────────────────────────────────────
                S_G4: begin
                    q2    <= q2 ^ q0;
                    state <= S_G5;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 5: T(q2) — phase +π/4
                // Forward torque. Phase interference begins building.
                // ──────────────────────────────────────────────────────────
                S_G5: begin
                    if (q2) phase2 <= phase2 + 3'd1;
                    state <= S_G6;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 6: CNOT(q1→q2): q2 ^= q1
                // Third entanglement — mirror of gate 2. Torque half-complete.
                // ──────────────────────────────────────────────────────────
                S_G6: begin
                    q2    <= q2 ^ q1;
                    state <= S_G7;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 7: T†(q2) — phase −π/4
                // Hold completes. Phase has rotated −π/4 net on q2.
                // ──────────────────────────────────────────────────────────
                S_G7: begin
                    if (q2) begin
                        phase2       <= phase2 - 3'd1;
                        remainder[2] <= remainder[2] ^ 1'b1;   // XOR: toggles T=1
                    end
                    state <= S_G8;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 8: CNOT(q0→q2): q2 ^= q0
                // Fourth entanglement. q2 interference half-resolved.
                // ──────────────────────────────────────────────────────────
                S_G8: begin
                    q2    <= q2 ^ q0;
                    state <= S_G9;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 9: T(q2) — phase +π/4
                // q2 phase path: 0 → +π → -π/4+π/4-π/4+π/4 = ... total: +π/2
                // ──────────────────────────────────────────────────────────
                S_G9: begin
                    if (q2) phase2 <= phase2 + 3'd1;
                    state <= S_G10;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 10: T(q1) — phase +π/4
                // Torque begins on control B. This is the 3-body coupling.
                // ──────────────────────────────────────────────────────────
                S_G10: begin
                    if (q1) begin
                        phase1     <= phase1 + 3'd1;
                        remainder[1] <= 1'b1;            // T=1 on qubit 1
                    end
                    state <= S_G11;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 11: CNOT(q0→q1): q1 ^= q0
                // Control qubits entangle. q1 becomes sensitive to q0.
                // ──────────────────────────────────────────────────────────
                S_G11: begin
                    q1    <= q1 ^ q0;
                    state <= S_G12;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 12: T†(q1) — phase −π/4
                // Reverse torque on q1. Remainder XOR toggles.
                // ──────────────────────────────────────────────────────────
                S_G12: begin
                    if (q1) begin
                        phase1       <= phase1 - 3'd1;
                        remainder[1] <= remainder[1] ^ 1'b1;
                    end
                    state <= S_G13;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 13: T(q0) — phase +π/4
                // Torque reaches control A. All three qubits now phase-coupled.
                // ──────────────────────────────────────────────────────────
                S_G13: begin
                    if (q0) begin
                        phase0     <= phase0 + 3'd1;
                        remainder[0] <= 1'b1;            // T=1 on qubit 0
                    end
                    state <= S_G14;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 14: CNOT(q0→q1): q1 ^= q0
                // Control qubits disentangle. q1 returns toward original state.
                // ──────────────────────────────────────────────────────────
                S_G14: begin
                    q1    <= q1 ^ q0;
                    state <= S_G15;
                end

                // ──────────────────────────────────────────────────────────
                // GATE 15: H(q2) — EXHALE
                // Hadamard collapses superposition. Phase interference resolves
                // into classical CCNOT: q2_out = q2_in XOR (q0 AND q1).
                // When q2_in = 1: q2_out = NAND(q0, q1)  ← default mode
                // When q2_in = 0: q2_out = AND (q0, q1)
                //
                // The NAND primitive resolves the collapse:
                //   nand_q0q1 = ~(q0 & q1)
                //   q2_out = q2_in ? nand_q0q1 : (q0 & q1)
                //
                // Shadow = cross-phase dissonance after collapse.
                // ──────────────────────────────────────────────────────────
                S_G15: begin
                    breath_exhale <= 1'b1;
                    // Collapse: H applies π phase then resolves
                    if (q2) phase2 <= phase2 + 3'd4;   // final π rotation
                    // CCNOT classical result via NAND primitive
                    q2    <= q2_in ? nand_q0q1 : (q0_in & q1_in);
                    // Shadow: XOR-sum of all phase accumulators
                    // Captures what the breath left unresolved
                    shadow <= (phase0 ^ phase1 ^ phase2) & 3'd7;
                    state <= S_OUT;
                end

                // ── OUTPUT: latch results, assert done ────────
                S_OUT: begin
                    q0_out <= q0;
                    q1_out <= q1;
                    q2_out <= q2;
                    done   <= 1'b1;
                    state  <= S_IDLE;
                end

                default: state <= S_IDLE;

            endcase
        end
    end

endmodule
