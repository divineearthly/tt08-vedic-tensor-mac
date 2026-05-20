module vedic_2x2 (
    input [1:0] a, b,
    output [3:0] p
);
    wire t1, t2, t3, t4, t5, t6;
    
    and (t1, a[0], b[0]);
    and (t2, a[1], b[0]);
    and (t3, a[0], b[1]);
    and (t4, a[1], b[1]);
    
    xor (t5, t2, t3);
    and (t6, t2, t3);
    
    assign p[0] = t1;
    assign p[1] = t5;
    xor (p[2], t4, t6);
    and (p[3], t4, t6);
endmodule
