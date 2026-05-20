module vedic_mac (
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [7:0] a,
    input wire [7:0] b,
    output reg [15:0] accum_out
);
    wire [15:0] product;

    // Instantiate your optimized 8x8 Vedic multiplier core
    vedic_mult_8x8 multiplier_core (
        .a(a),
        .b(b),
        .p(product)
    );

    // Synchronous accumulation logic
    always @(posedge clk) begin
        if (rst) begin
            accum_out <= 16'b0;
        end else if (valid_in) begin
            accum_out <= accum_out + product;
        end
    end
endmodule
