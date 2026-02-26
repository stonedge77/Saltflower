// ================================================================
// Testbench: NAND NEEDLE 8-bit Core with Full Friction Scanner
// Tests real board init, move sequence, friction computation & slip
// ================================================================

`timescale 1ns / 1ps

module tb_nand_needle_8bit_friction;

    // ------------------------------------------------------------
    // DUT signals
    // ------------------------------------------------------------
    reg         clk;
    reg         rst_n;
    reg         step;
    reg         player_move;
    reg  [5:0]  player_from;
    reg  [5:0]  player_to;
    wire [7:0]  remainder;
    wire [2:0]  phase;
    wire        slip_detected;
    wire [7:0]  needle_mask;
    wire [5:0]  ai_from;
    wire [5:0]  ai_to;
    wire        ai_valid;

    // ------------------------------------------------------------
    // Instantiate DUT
    // ------------------------------------------------------------
    nand_needle_8bit dut (
        .clk            (clk),
        .rst_n          (rst_n),
        .step           (step),
        .player_move    (player_move),
        .player_from    (player_from),
        .player_to      (player_to),
        .remainder      (remainder),
        .phase          (phase),
        .slip_detected  (slip_detected),
        .needle_mask    (needle_mask),
        .ai_from        (ai_from),
        .ai_to          (ai_to),
        .ai_valid       (ai_valid)
    );

    // ------------------------------------------------------------
    // Clock: 50 MHz (20 ns period)
    // ------------------------------------------------------------
    initial begin
        clk = 0;
        forever #10 clk = ~clk;
    end

    // ------------------------------------------------------------
    // Helper: Apply move (simplified — no legality check here)
    // Sets piece at 'to', clears 'from'
    // ------------------------------------------------------------
    task apply_move;
        input [5:0] from_sq;
        input [5:0] to_sq;
        begin
            // Get piece from 'from'
            reg [3:0] moving_piece = dut.get_piece(from_sq);
            // Clear from
            dut.set_piece(from_sq, 4'd0);
            // Place at 'to' (capture overwrites)
            dut.set_piece(to_sq, moving_piece);
            $display("Applied move: %0d → %0d  (piece: %h)", from_sq, to_sq, moving_piece);
        end
    endtask

    // ------------------------------------------------------------
    // Stimulus: Real opening sequence + friction observation
    // ------------------------------------------------------------
    initial begin
        // Initialize
        rst_n       = 0;
        step        = 0;
        player_move = 0;
        player_from = 6'd0;
        player_to   = 6'd0;

        // Reset
        #100;
        rst_n = 1;
        #200;

        // ==============================================
        // Initialize starting position (frame 0)
        // White on ranks 1-2, Black on 7-8
        // =============================================================
        // Rooks: a1=1000 (R white), h1=1000, a8=1100 (R black), h8=1100
        // Knights: b1=0100, g1=0100, b8=0100, g8=0100
        // Bishops: c1=0110, f1=0110, c8=0110, f8=0110
        // Queen: d1=1010, d8=1010
        // King: e1=1100, e8=1100
        // Pawns: rank 2 & 7 all 0001/1001
        // =============================================================
        // (This is tedious — in real code use $readmemh or init block)
        // For brevity, only set key squares + pawns approximated

        // White back rank (rank 0)
        dut.set_piece(6'd0,  4'b1000); // a1 R
        dut.set_piece(6'd1,  4'b0100); // b1 N
        dut.set_piece(6'd2,  4'b0110); // c1 B
        dut.set_piece(6'd3,  4'b1010); // d1 Q
        dut.set_piece(6'd4,  4'b1100); // e1 K
        dut.set_piece(6'd5,  4'b0110); // f1 B
        dut.set_piece(6'd6,  4'b0100); // g1 N
        dut.set_piece(6'd7,  4'b1000); // h1 R

        // Black back rank (rank 7)
        dut.set_piece(6'd56, 4'b1100); // a8 r
        dut.set_piece(6'd57, 4'b0100); // b8 n
        dut.set_piece(6'd58, 4'b0110); // c8 b
        dut.set_piece(6'd59, 4'b1010); // d8 q
        dut.set_piece(6'd60, 4'b1100); // e8 k
        dut.set_piece(6'd61, 4'b0110); // f8 b
        dut.set_piece(6'd62, 4'b0100); // g8 n
        dut.set_piece(6'd63, 4'b1100); // h8 r

        // Pawns (all white rank 1=0001, black rank 6=1001)
        for (integer f = 0; f < 8; f = f + 1) begin
            dut.set_piece(6'd(f + 8),  4'b0001);  // rank 1 white pawns
            dut.set_piece(6'd(f + 48), 4'b1001);  // rank 6 black pawns
        end

        $display("Starting position loaded. Initial friction scan will run on first step.");

        // ==============================================
        // Run simulation: apply moves + step
        // ==============================================
        #100;

        $display("Time\tPhase\tRem\tSlip\tNeedle\tAvgFric\tDelta\tAI move");
        $monitor("%t\t%0d\t%h\t%b\t%h\t%0.2f\t%0.2f\t%0d→%0d (%b)",
                 $time, phase, remainder, slip_detected, needle_mask,
                 $itor(dut.curr_min_res)/16.0, $itor(dut.curr_min_res - dut.prev_min_res)/16.0,
                 ai_from, ai_to, ai_valid);

        // Step 1: trigger initial friction scan
        step = 1; #20; step = 0; #80;

        // Move 1: white e4 (e2=12 → e4=28)
        apply_move(6'd12, 6'd28);
        step = 1; #20; step = 0; #80;

        // Move 2: black e5 (e7=52 → e5=36)
        apply_move(6'd52, 6'd36);
        step = 1; #20; step = 0; #80;

        // Move 3: white Nf3 (g1=6 → f3=21)
        apply_move(6'd6, 6'd21);
        step = 1; #20; step = 0; #80;

        // Move 4: black Nc6 (b8=57 → c6=42)
        apply_move(6'd57, 6'd42);
        step = 1; #20; step = 0; #80;

        // Move 5: white d4 (d2=11 → d4=27)
        apply_move(6'd11, 6'd27);
        step = 1; #20; step = 0; #80;

        // Move 6: black exd4 (e5=36 → d4=27 capture)
        apply_move(6'd36, 6'd27);
        step = 1; #20; step = 0; #80;

        // Move 7: white Nxd4 (f3=21 → d4=27 capture)
        apply_move(6'd21, 6'd27);
        step = 1; #20; step = 0; #80;

        // Run extra steps to observe oscillation
        repeat(6) begin
            #100;
            step = 1; #20; step = 0; #80;
        end

        $display("\n=== TEST COMPLETE ===");
        $display("Final remainder: 0x%h", remainder);
        $display("Final phase: %0d", phase);
        $display("Slip occurred: %b", slip_detected);
        $display("Final needle mask: 0x%h", needle_mask);

        #500;
        $finish;
    end

    // ------------------------------------------------------------
    // Dump waveform
    // ------------------------------------------------------------
    initial begin
        $dumpfile("nand_needle_friction_tb.vcd");
        $dumpvars(0, tb_nand_needle_8bit_friction);
    end

endmodule
