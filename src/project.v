`default_nettype none

// Attach the optimized arithmetic building blocks for hierarchical hardware compilation
`include "vedic_2x2.v"
`include "vedic_mult_4x4_opt.v"
`include "vedic_mult_8x8_opt.v"
`include "vedic_mac.v"

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs: Operand A [7:0]
    output wire [7:0] uo_out,   // Dedicated outputs: Accumulator Lower Byte [7:0]
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path: Accumulator Upper Byte [7:0]
    output wire [7:0] uio_oe,   // IOs: Enable path (1 = output, 0 = input)
    input  wire       ena,      // High when code block is dynamically active
    input  wire       clk,      // System hardware clock
    input  wire       rst_n     // Active-low asynchronous hardware reset
);

    wire sys_rst = !rst_n;
    wire [15:0] master_accum;

    // Lock all bi-directional IOs to handle high-byte data streaming
    assign uio_oe  = 8'b11111111; 
    assign uo_out  = master_accum[7:0];
    assign uio_out = master_accum[15:8];

    // Instantiate your 26-gate structural Vedic MAC processing block
    vedic_mac native_mac (
        .clk(clk),
        .rst(sys_rst),
        .valid_in(ena),
        .a(ui_in),
        .b(ui_in), 
        .accum_out(master_accum)
    );

endmodule
