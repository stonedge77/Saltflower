// ================================================================
// NAND NEEDLE - 8-bit Core Skeleton with Full 64-Square Memory & Friction Scanner
// Each square: 4-bit encoding (3-bit piece type + 1-bit color)
// Piece types: 000=empty, 001=P, 010=N, 011=B, 100=R, 101=Q, 110=K (111 reserved)
// Color: 0=white, 1=black
// Total per frame: 64 squares × 4 bits = 256 bits = 32 bytes (as before)
// Friction scanner: full 64 squares, each with 3-bit friction (sum of opp/same neighbors)
// ================================================================

`timescale 1ns / 1ps

module nand_needle_8bit (
    input  wire        clk,             // system clock (e.g. 12–50 MHz)
    input  wire        rst_n,           // active-low reset
    input  wire        step,            // pulse = make one move / advance phase
    input  wire        player_move,     // 1 = player just moved (needle guidance)
    input  wire [5:0]  player_from,     // 0–63 square (6-bit)
    input  wire [5:0]  player_to,       // 0–63 square
    output reg  [7:0]  remainder,       // current 8-bit ring remainder
    output reg  [2:0]  phase,           // 0–7 phase counter
    output reg         slip_detected,   // high when delta <= threshold
    output reg  [7:0]  needle_mask,     // 8-bit mask: which diag dirs to prefer
    output reg  [5:0]  ai_from,         // AI chosen move
    output reg  [5:0]  ai_to,
    output reg         ai_valid         // high when AI has a move ready
);

// ---------------------------------------------------------------
// Memory: 8 frames × 32 bytes = 256 bytes (8-bit addressed)
// Each byte stores 2 squares (4 bits each): [7:4]=sq_even, [3:0]=sq_odd
// ---------------------------------------------------------------
reg [7:0] frame_mem [0:255];            // 256 × 8-bit = 2 KiB
wire [7:0] current_base = {phase, 5'b00000};  // phase << 5 = ×32

// Helper: Get piece at square addr (0–63)
function [3:0] get_piece;
    input [5:0] addr;
    reg [7:0] byte_addr = addr[5:1];  // divide by 2
    reg [7:0] mem_val = frame_mem[current_base + byte_addr];
    get_piece = addr[0] ? mem_val[3:0] : mem_val[7:4];
endfunction

// Set piece at square addr
task set_piece;
    input [5:0] addr;
    input [3:0] val;
    reg [7:0] byte_addr = addr[5:1];
    reg [7:0] mem_val = frame_mem[current_base + byte_addr];
    if (addr[0]) mem_val[3:0] = val;
    else mem_val[7:4] = val;
    frame_mem[current_base + byte_addr] = mem_val;
endtask

// ---------------------------------------------------------------
// Registers (unchanged)
// ---------------------------------------------------------------
reg [7:0] ring_cells     [0:7];         // 8 NAND cells
reg [7:0] prev_min_res;
reg [7:0] curr_min_res;                 // 8-bit fixed-point approx

// Friction: 64 × 3-bit values, packed into 24 bytes (8-bit regs, but accessed as array)
// For simplicity, use reg [2:0] friction [0:63] — synthesizer will pack
reg [2:0] friction [0:63];              // 64 × 3-bit = 192 bits

// ---------------------------------------------------------------
// Phase counter (unchanged)
// ---------------------------------------------------------------
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        phase <= 3'd0;
    end else if (step) begin
        phase <= phase + 1'b1;          // naturally wraps at 8 → 0
    end
end

// ---------------------------------------------------------------
// Cyclic NAND Ring (unchanged)
// ---------------------------------------------------------------
wire [7:0] probe_inputs;
assign probe_inputs = {get_piece(6'd0)[0], get_piece(6'd9)[0], get_piece(6'd18)[0], get_piece(6'd27)[0],
                       get_piece(6'd36)[0], get_piece(6'd45)[0], get_piece(6'd54)[0], get_piece(6'd63)[0]};  // example: a1-h8 diag LSBs

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        for (integer i = 0; i < 8; i = i + 1) ring_cells[i] <= 8'd0;
        remainder <= 8'd0;
    end else if (step) begin
        for (integer i = 0; i < 8; i = i + 1) begin
            wire a = probe_inputs[i];
            wire b = (i == 0) ? remainder[0] : ring_cells[i-1][0];
            wire nand_ab = ~(a & b);
            wire t = a ^ b ^ nand_ab;
            ring_cells[i] <= {ring_cells[i][6:0], nand_ab};  // shift left, new LSB
            remainder[i] <= t;                              // parity collection
        end
    end
end

// ---------------------------------------------------------------
// Real Friction Scanner: Full 64 Squares
// For each square, sum opposing/same neighbors (up to 8), saturate to 3-bit (0–7)
// Synthesizable: Use generate loop for unrolled computation (avoids dynamic loops)
// ---------------------------------------------------------------
genvar s;
generate
    for (s = 0; s < 64; s = s + 1) begin : friction_gen
        always @(posedge clk or negedge rst_n) begin
            if (!rst_n) begin
                friction[s] <= 3'd0;
            end else if (step) begin
                wire [3:0] piece = get_piece(s);
                if (piece == 4'd0) begin  // empty
                    friction[s] <= 3'd0;
                end else begin
                    wire color = piece[3];  // MSB = color
                    wire opp = ~color;
                    reg [3:0] fric_sum = 4'd0;
                    genvar dr, df;
                    for (dr = -1; dr <= 1; dr = dr + 1) begin : dr_loop
                        for (df = -1; df <= 1; df = df + 1) begin : df_loop
                            if (dr == 0 && df == 0) begin
                                // skip self
                            end else begin
                                localparam integer nr = (s / 8) + dr;
                                localparam integer nf = (s % 8) + df;
                                if (nr >= 0 && nr < 8 && nf >= 0 && nf < 8) begin
                                    localparam integer ns = nr * 8 + nf;
                                    wire [3:0] n_piece = get_piece(ns);
                                    if (n_piece != 4'd0) begin
                                        if (n_piece[3] == opp) fric_sum = fric_sum + 4'd2;
                                        else fric_sum = fric_sum + 4'd1;
                                    end
                                end
                            end
                        end
                    end
                    friction[s] <= fric_sum > 4'd7 ? 3'd7 : fric_sum[2:0];  // saturate to 3-bit
                end
            end
        end
    end
endgenerate

// ---------------------------------------------------------------
// Min resistance & slip detection (unchanged from skeleton)
// ---------------------------------------------------------------
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        prev_min_res   <= 8'd64;        // mid-range initial
        curr_min_res   <= 8'd64;
        slip_detected  <= 1'b0;
        needle_mask    <= 8'h00;
    end else if (step) begin
        // Simplified: find min avg friction over 8 sample rays
        reg [7:0] min_avg = 8'hFF;
        reg [7:0] min_dir = 8'h00;
        integer dir, start;
        for (dir = 0; dir < 4; dir = dir + 1) begin  // 4 diag dirs
            integer dr = (dir==0 ? 1: (dir==1 ? 1: (dir==2 ? -1: -1)));
            integer df = (dir==0 ? 1: (dir==1 ? -1: (dir==2 ? 1: -1)));
            for (start = 0; start < 8; start = start + 1) begin  // 8 starts per dir
                reg [10:0] sum = 0;
                reg [3:0] len = 0;
                integer r = start, f = start;  // example starts on diag
                while (r >= 0 && r < 8 && f >= 0 && f < 8 && len < 8) begin
                    integer s = r * 8 + f;
                    if (get_piece(s) != 4'd0) break;  // open only
                    sum = sum + {5'b0, friction[s]};
                    len = len + 1;
                    r = r + dr;
                    f = f + df;
                end
                if (len > 0) begin
                    reg [7:0] avg = sum / len;  // integer div
                    if (avg < min_avg) begin
                        min_avg = avg;
                        min_dir = 1 << dir;  // bit for dir
                    end
                end
            end
        end
        curr_min_res <= min_avg;

        // Delta in 2's complement
        wire signed [8:0] delta = curr_min_res - prev_min_res;
        prev_min_res <= curr_min_res;

        if (delta <= -9'sd2) begin
            slip_detected <= 1'b1;
            needle_mask <= min_dir;  // prefer the lowest dir(s)
        end else begin
            slip_detected <= slip_detected;  // latch
        end
    end
end

// ---------------------------------------------------------------
// AI move selector (unchanged)
// ---------------------------------------------------------------
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ai_from   <= 6'd0;
        ai_to     <= 6'd0;
        ai_valid  <= 1'b0;
    end else if (step && slip_detected) begin
        // Example: choose from/to based on mask & remainder
        reg [5:0] candidate_from = remainder[7:2];  // use upper bits as from
        reg [5:0] candidate_to   = remainder[5:0];  // lower as to offset
        ai_from <= candidate_from;
        ai_to   <= candidate_from + (needle_mask & 8'h0F);  // bias by mask
        ai_valid<= 1'b1;
    end else begin
        ai_valid <= 1'b0;
    end
end

endmodule
