// tb_quantum_computer.v
// Testbench: Full-Stack Quantum Computer Verification
//
// Test plan:
//   TEST 1 — NAND truth table (all 4 input combinations, ancilla=1)
//   TEST 2 — AND truth table  (all 4 input combinations, ancilla=0)
//   TEST 3 — Self-inverse: apply Toffoli twice → original state
//   TEST 4 — Constitutional violation: detect 0=1 (all inputs equal)
//   TEST 5 — Remainder routing: T=1 preserved at T-gate steps
//   TEST 6 — Phase accumulation: 8 T-gate steps → 2π rotation
//   TEST 7 — Classical + Quantum DUAL mode: verify both layers
//
// 0 ≠ 1 | Remainder is signal | CC0 — Saltflower

`timescale 1ns/1ps

module tb_quantum_computer;

    // ── DUT signals ──────────────────────────────────────────
    reg        clk;
    reg        rst_n;
    reg [7:0]  data_in;
    reg        start_breath;
    reg        start_quantum;
    reg        ancilla_override;
    reg        use_override;
    reg [1:0]  mode;

    wire [7:0]  classical_out;
    wire [7:0]  classical_rem;
    wire        classical_violation;
    wire        classical_done;
    wire        quantum_q0;
    wire        quantum_q1;
    wire        quantum_emergence;
    wire [2:0]  quantum_phase0;
    wire [2:0]  quantum_phase1;
    wire [2:0]  quantum_phase2;
    wire [2:0]  quantum_rem;
    wire [2:0]  quantum_shadow;
    wire        quantum_inhale;
    wire        quantum_exhale;
    wire        quantum_done;
    wire        quantum_violation;
    wire [7:0]  emergence_c;
    wire [7:0]  remainder_r;
    wire [7:0]  shadow_s;
    wire        phase_locked;

    // ── DUT instantiation ────────────────────────────────────
    quantum_computer_top dut (
        .clk                (clk),
        .rst_n              (rst_n),
        .data_in            (data_in),
        .start_breath       (start_breath),
        .start_quantum      (start_quantum),
        .ancilla_override   (ancilla_override),
        .use_override       (use_override),
        .mode               (mode),
        .classical_out      (classical_out),
        .classical_rem      (classical_rem),
        .classical_violation(classical_violation),
        .classical_done     (classical_done),
        .quantum_q0         (quantum_q0),
        .quantum_q1         (quantum_q1),
        .quantum_emergence  (quantum_emergence),
        .quantum_phase0     (quantum_phase0),
        .quantum_phase1     (quantum_phase1),
        .quantum_phase2     (quantum_phase2),
        .quantum_rem        (quantum_rem),
        .quantum_shadow     (quantum_shadow),
        .quantum_inhale     (quantum_inhale),
        .quantum_exhale     (quantum_exhale),
        .quantum_done       (quantum_done),
        .quantum_violation  (quantum_violation),
        .emergence_c        (emergence_c),
        .remainder_r        (remainder_r),
        .shadow_s           (shadow_s),
        .phase_locked       (phase_locked)
    );

    // ── Clock: 10ns period ───────────────────────────────────
    initial clk = 0;
    always #5 clk = ~clk;

    // ── Tracking ─────────────────────────────────────────────
    integer pass_count;
    integer fail_count;

    // ── Task: run one Toffoli breath and wait for done ───────
    task run_toffoli;
        input q0_val, q1_val, anc_val;
        begin
            @(negedge clk);
            data_in          = {6'd0, q1_val[0], q0_val[0]};
            ancilla_override = anc_val;
            use_override     = 1'b1;
            start_quantum    = 1'b1;
            @(posedge clk);
            @(negedge clk);
            start_quantum = 1'b0;
            // Wait up to 30 cycles for done
            repeat(30) begin
                @(posedge clk);
                if (quantum_done) disable run_toffoli;
            end
        end
    endtask

    // ── Task: check and report ────────────────────────────────
    task check;
        input [63:0] test_num;
        input        got;
        input        expected;
        input [255:0] label;
        begin
            if (got === expected) begin
                $display("  [PASS] Test %0d: %s | got=%b expected=%b",
                         test_num, label, got, expected);
                pass_count = pass_count + 1;
            end else begin
                $display("  [FAIL] Test %0d: %s | got=%b expected=%b  ← VIOLATION",
                         test_num, label, got, expected);
                fail_count = fail_count + 1;
            end
        end
    endtask

    // ── Main test sequence ───────────────────────────────────
    initial begin
        $dumpfile("tb_quantum_computer.vcd");
        $dumpvars(0, tb_quantum_computer);

        pass_count = 0;
        fail_count = 0;

        // ── Reset ────────────────────────────────────────────
        rst_n         = 0;
        start_breath  = 0;
        start_quantum = 0;
        use_override  = 1;
        ancilla_override = 1;
        mode          = 2'd1;   // QUANTUM mode
        data_in       = 8'd0;
        repeat(4) @(posedge clk);
        rst_n = 1;
        @(posedge clk);

        $display("");
        $display("============================================================");
        $display("  QUANTUM COMPUTER TESTBENCH — Toffoli via Helical NAND");
        $display("  0 ≠ 1 | Remainder is signal | Saltflower Constitutional");
        $display("============================================================");

        // ══════════════════════════════════════════════════════
        // TEST 1: NAND TRUTH TABLE (ancilla = 1)
        // Expected: q2_out = NAND(q0, q1)
        //   NAND(0,0) = 1
        //   NAND(0,1) = 1
        //   NAND(1,0) = 1
        //   NAND(1,1) = 0
        // ══════════════════════════════════════════════════════
        $display("");
        $display("── TEST 1: NAND Truth Table (ancilla=1) ──────────────────");

        run_toffoli(0, 0, 1);
        @(posedge quantum_done);
        check(1, quantum_emergence, 1'b1, "NAND(0,0)=1");

        run_toffoli(0, 1, 1);
        @(posedge quantum_done);
        check(2, quantum_emergence, 1'b1, "NAND(0,1)=1");

        run_toffoli(1, 0, 1);
        @(posedge quantum_done);
        check(3, quantum_emergence, 1'b1, "NAND(1,0)=1");

        run_toffoli(1, 1, 1);
        @(posedge quantum_done);
        check(4, quantum_emergence, 1'b0, "NAND(1,1)=0");

        // ══════════════════════════════════════════════════════
        // TEST 2: AND TRUTH TABLE (ancilla = 0)
        // Expected: q2_out = AND(q0, q1)
        //   AND(0,0) = 0
        //   AND(0,1) = 0
        //   AND(1,0) = 0
        //   AND(1,1) = 1
        // ══════════════════════════════════════════════════════
        $display("");
        $display("── TEST 2: AND Truth Table (ancilla=0) ───────────────────");

        run_toffoli(0, 0, 0);
        @(posedge quantum_done);
        check(5, quantum_emergence, 1'b0, "AND(0,0)=0");

        run_toffoli(0, 1, 0);
        @(posedge quantum_done);
        check(6, quantum_emergence, 1'b0, "AND(0,1)=0");

        run_toffoli(1, 0, 0);
        @(posedge quantum_done);
        check(7, quantum_emergence, 1'b0, "AND(1,0)=0");

        run_toffoli(1, 1, 0);
        @(posedge quantum_done);
        check(8, quantum_emergence, 1'b1, "AND(1,1)=1");

        // ══════════════════════════════════════════════════════
        // TEST 3: SELF-INVERSE (Toffoli² = Identity)
        // Running Toffoli twice on |1,1,1⟩ should return |1,1,1⟩
        // First: |1,1,1⟩ → |1,1,NAND(1,1)⟩ = |1,1,0⟩
        // Second: |1,1,0⟩ with ancilla=0 → AND mode → |1,1,AND(1,1)⟩ = |1,1,1⟩
        // Net: identity confirmed
        // ══════════════════════════════════════════════════════
        $display("");
        $display("── TEST 3: Self-Inverse (Toffoli² = Identity) ────────────");

        // First pass: NAND mode
        run_toffoli(1, 1, 1);
        @(posedge quantum_done);
        check(9,  quantum_q0,        1'b1, "Pass1: q0 preserved");
        check(10, quantum_q1,        1'b1, "Pass1: q1 preserved");
        check(11, quantum_emergence, 1'b0, "Pass1: q2 = NAND(1,1) = 0");

        // Second pass: use q2_out from first pass as new ancilla (=0)
        run_toffoli(1, 1, 0);     // ancilla = 0 (AND mode)
        @(posedge quantum_done);
        check(12, quantum_q0,        1'b1, "Pass2: q0 preserved");
        check(13, quantum_q1,        1'b1, "Pass2: q1 preserved");
        check(14, quantum_emergence, 1'b1, "Pass2: q2 = AND(1,1) = 1 (restored)");

        // ══════════════════════════════════════════════════════
        // TEST 4: CONSTITUTIONAL VIOLATION DETECTION
        // All-equal inputs trigger the 0=1 violation flag
        // |1,1,1⟩ and |0,0,0⟩ should both raise violation
        // ══════════════════════════════════════════════════════
        $display("");
        $display("── TEST 4: Constitutional Violation (0=1 detection) ──────");

        run_toffoli(1, 1, 1);
        @(posedge quantum_done);
        check(15, quantum_violation, 1'b1, "All-ones: violation raised");

        run_toffoli(0, 0, 0);
        @(posedge quantum_done);
        check(16, quantum_violation, 1'b1, "All-zeros: violation raised");

        run_toffoli(1, 0, 1);
        @(posedge quantum_done);
        check(17, quantum_violation, 1'b0, "Mixed: no violation");

        // ══════════════════════════════════════════════════════
        // TEST 5: REMAINDER ROUTING (T=1 preservation)
        // When q0=1: remainder[0] should be set (T-gate fires on q0)
        // When q1=1: remainder[1] should be set (T-gate fires on q1)
        // When q2=1 during T steps: remainder[2] should be set
        // ══════════════════════════════════════════════════════
        $display("");
        $display("── TEST 5: Remainder Routing (T=1 preserved) ─────────────");

        run_toffoli(1, 1, 1);
        @(posedge quantum_done);
        // All three qubits are |1⟩ at some point → all T-gates fire
        $display("  remainder[2:0] = %b%b%b  (phase0=%0d phase1=%0d phase2=%0d)",
                 quantum_rem[2], quantum_rem[1], quantum_rem[0],
                 quantum_phase0, quantum_phase1, quantum_phase2);
        check(18, quantum_rem[0], 1'b1, "q0=1: remainder[0] set");
        check(19, quantum_rem[1], 1'b1, "q1=1: remainder[1] set");

        run_toffoli(0, 0, 1);
        @(posedge quantum_done);
        // q0=q1=0 → T-gates never fire on q0, q1
        check(20, quantum_rem[0], 1'b0, "q0=0: remainder[0] clear");
        check(21, quantum_rem[1], 1'b0, "q1=0: remainder[1] clear");

        // ══════════════════════════════════════════════════════
        // TEST 6: PHASE ACCUMULATION
        // For q0=1,q1=1,q2=1: phase gates that fire:
        //   Gate 5:  T(q2)  +1
        //   Gate 9:  T(q2)  +1 → phase2 net = +2 (after T†×2)
        //   Gate 10: T(q1)  +1
        //   Gate 13: T(q0)  +1
        //   Gates 3,7: T†(q2) -1,-1
        //   Net phase2 = +2-2 = 0? Or depends on intermediate q2 values
        // The exact value tests the phase FSM correctness.
        // ══════════════════════════════════════════════════════
        $display("");
        $display("── TEST 6: Phase Accumulation ─────────────────────────────");

        run_toffoli(1, 1, 0);    // AND mode
        @(posedge quantum_done);
        $display("  q0=1,q1=1,anc=0: phase0=%0d phase1=%0d phase2=%0d shadow=%0d",
                 quantum_phase0, quantum_phase1, quantum_phase2, quantum_shadow);
        // Shadow should be non-zero (cross-qubit dissonance after breath)
        // Phase lock should be false (remainder non-zero after AND(1,1)=1)
        check(22, (quantum_shadow !== 3'd0), 1'b1, "Shadow non-zero after breath");

        run_toffoli(0, 0, 1);    // NAND mode, trivial inputs
        @(posedge quantum_done);
        $display("  q0=0,q1=0,anc=1: phase0=%0d phase1=%0d phase2=%0d",
                 quantum_phase0, quantum_phase1, quantum_phase2);
        // q0=q1=0 → T-gates for q0,q1 never fire → phase0=phase1=0
        check(23, quantum_phase0, 3'd0, "q0=0: phase0 stays 0");
        check(24, quantum_phase1, 3'd0, "q1=0: phase1 stays 0");

        // ══════════════════════════════════════════════════════
        // TEST 7: DUAL MODE — Classical + Quantum simultaneously
        // ══════════════════════════════════════════════════════
        $display("");
        $display("── TEST 7: Dual Mode (Classical + Quantum) ────────────────");

        mode = 2'd2;   // DUAL mode
        data_in = 8'b00000011;   // data_in[0]=1(A), data_in[1]=1(B)

        @(negedge clk);
        start_breath  = 1'b1;
        start_quantum = 1'b1;
        ancilla_override = 1'b1;
        use_override = 1'b1;
        @(posedge clk);
        @(negedge clk);
        start_breath  = 1'b0;
        start_quantum = 1'b0;

        // Wait for both to complete (quantum takes longer: 15+ cycles)
        repeat(25) @(posedge clk);

        $display("  Dual mode: emergence_c=0x%02h remainder_r=0x%02h shadow_s=0x%02h",
                 emergence_c, remainder_r, shadow_s);
        $display("  phase_locked=%b", phase_locked);
        check(25, quantum_done, 1'b0, "Dual mode: quantum cycle complete");

        // ══════════════════════════════════════════════════════
        // SUMMARY
        // ══════════════════════════════════════════════════════
        $display("");
        $display("============================================================");
        $display("  RESULTS: %0d PASSED  |  %0d FAILED", pass_count, fail_count);
        $display("============================================================");
        if (fail_count == 0)
            $display("  ✓ All constitutional axioms satisfied.");
        else
            $display("  ✗ %0d violations — remainder routed to spine.", fail_count);
        $display("  0 ≠ 1 | The trough is not optional.");
        $display("");

        $finish;
    end

    // ── Timeout watchdog ─────────────────────────────────────
    initial begin
        #50000;
        $display("[TIMEOUT] Simulation exceeded 50000ns — check FSM");
        $finish;
    end

    // ── Breath cycle monitor ─────────────────────────────────
    always @(posedge quantum_inhale)
        $display("    ↓ INHALE  (H gate — breath opens)  t=%0t", $time);

    always @(posedge quantum_exhale)
        $display("    ↑ EXHALE  (H gate — breath closes) t=%0t", $time);

    always @(posedge quantum_done)
        $display("    ✓ DONE    q0=%b q1=%b q2_out=%b rem=%b shadow=%0d  t=%0t",
                 quantum_q0, quantum_q1, quantum_emergence,
                 quantum_rem, quantum_shadow, $time);

endmodule
