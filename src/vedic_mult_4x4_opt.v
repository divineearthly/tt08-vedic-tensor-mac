module vedic_mult_4x4 (
    input [3:0] a, b,
    output [7:0] p
);
    wire [3:0] pp0, pp1, pp2, pp3;
    
    vedic_2x2 v00 (a[1:0], b[1:0], pp0);
    vedic_2x2 v01 (a[3:2], b[1:0], pp1);
    vedic_2x2 v02 (a[1:0], b[3:2], pp2);
    vedic_2x2 v03 (a[3:2], b[3:2], pp3);
    
    // Use explicit bit manipulation so Yosys sees the parallelism
    wire [7:0] summand0 = {4'b0, pp0};
    wire [7:0] summand1 = {2'b0, pp1, 2'b0};
    wire [7:0] summand2 = {2'b0, pp2, 2'b0};
    wire [7:0] summand3 = {pp3, 4'b0};
    
    // Give Yosys all four terms simultaneously — let it build the Wallace tree
    assign p = summand0 + summand1 + summand2 + summand3;
endmodule
