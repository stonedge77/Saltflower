// helical_nand_array.v
// 8 cells in π/4 rotational increments

module helical_nand_array (
    input wire clk,
    input wire rst_n,
    
    // Input interface
    input wire [7:0] data_in,
    input wire start_breath,
    
    // Output interface
    output wire [7:0] data_out,
    output wire [7:0] remainders,  // T=1 bits
    output wire any_violation,
    output wire breath_complete
);

    // Breath cycle orchestrator
    reg [1:0] breath_phase;
    reg [2:0] cell_counter;
    
    wire inhale = (breath_phase == 2'd0);
    wire exhale = (breath_phase == 2'd2);
    
    // Cell interconnect
    wire [7:0] signal_chain;
    wire [2:0] phase_chain [7:0];
    wire [7:0] admit_chain;
    wire [7:0] violation_flags;
    wire [7:0] remainder_bits;
    
    // Instantiate 8 helical cells
    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : helix
            helical_nand_cell #(
                .PHASE_BITS(3)
            ) cell (
                .clk(clk),
                .rst_n(rst_n),
                
                // Chain signals helically
                .signal_in(i == 0 ? data_in[0] : signal_chain[i-1]),
                .signal_out(signal_chain[i]),
                
                // Phase propagation (rotates π/4 each cell)
                .phase_in(i == 0 ? 3'd0 : phase_chain[i-1]),
                .phase_out(phase_chain[i]),
                
                // Constitutional check
                .admit(admit_chain[i]),
                .violation(violation_flags[i]),
                
                // Breath control
                .inhale(inhale),
                .exhale(exhale),
                .remainder(remainder_bits[i])
            );
        end
    endgenerate
    
    // Admission logic (0≠1 enforcement)
    // Each cell checks if input ≠ potential
    assign admit_chain = ~(data_in ^ {signal_chain[6:0], data_in[7]});
    
    // Aggregate outputs
    assign data_out = signal_chain;
    assign remainders = remainder_bits;
    assign any_violation = |violation_flags;
    
    // Breath cycle control
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            breath_phase <= 2'd0;
            cell_counter <= 3'd0;
        end else if (start_breath) begin
            breath_phase <= 2'd0;
            cell_counter <= 3'd0;
        end else if (cell_counter < 3'd7) begin
            cell_counter <= cell_counter + 1;
        end else begin
            breath_phase <= breath_phase + 1;
            if (breath_phase == 2'd3) begin
                breath_phase <= 2'd0;  // Return to zero
            end
        end
    end
    
    assign breath_complete = (breath_phase == 2'd3);
    
endmodule
