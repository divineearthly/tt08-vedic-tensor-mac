module vedic_mult_8x8 (
    input [7:0] a, b,
    output [15:0] p
);
    wire [7:0] pp0, pp1, pp2, pp3;
    
    vedic_mult_4x4 v00 (a[3:0], b[3:0], pp0);
    vedic_mult_4x4 v01 (a[7:4], b[3:0], pp1);
    vedic_mult_4x4 v02 (a[3:0], b[7:4], pp2);
    vedic_mult_4x4 v03 (a[7:4], b[7:4], pp3);
    
    // All four terms aligned in a single expression
    wire [15:0] summand0 = {8'b0, pp0};
    wire [15:0] summand1 = {4'b0, pp1, 4'b0};
    wire [15:0] summand2 = {4'b0, pp2, 4'b0};
    wire [15:0] summand3 = {pp3, 8'b0};
    
    // Single multi-operand addition — Yosys + ABC can optimize this aggressively
    assign p = summand0 + summand1 + summand2 + summand3;
endmodule
