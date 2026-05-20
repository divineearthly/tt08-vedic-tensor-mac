`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs: Operand A/B vector [7:0]
    output wire [7:0] uo_out,   // Dedicated outputs: Accumulator Lower Byte [7:0]
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path: Accumulator Upper Byte [7:0]
    output wire [7:0] uio_oe,   // IOs: Enable path (1 = output, 0 = input)
    input  wire       ena,      // High when cell slot is active
    input  wire       clk,      // System hardware clock
    input  wire       rst_n     // Active-low asynchronous reset
);

    wire sys_rst = !rst_n;
    wire [15:0] master_accum;

    // Route all bidirectional IO pins to strictly operate as high-byte data outputs
    assign uio_oe  = 8'b11111111; 
    assign uo_out  = master_accum[7:0];
    assign uio_out = master_accum[15:8];

    // Instantiate your 26-gate-depth Vedic MAC core
    vedic_mac native_mac (
        .clk(clk),
        .rst(sys_rst),
        .valid_in(ena),
        .a(ui_in),
        .b(ui_in), 
        .accum_out(master_accum)
    );

endmodule
