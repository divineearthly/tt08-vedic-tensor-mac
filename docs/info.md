## How it works

This design implements an 8-bit hardware Multiply-Accumulate (MAC) unit optimized for tensor arithmetic. It replaces standard sequential Booth/Wallace multiplier architectures with a purely structural hierarchical execution grid based on the Vedic mathematics sutra 'Urdhva Tiryagbhyam' (Vertically and Crosswise).

The internal multiplier scales recursively: four 2x2 bit pure gate-level matrices feed parallel 4x4 bit blocks, which are combined into an 8x8 core via a balanced adder tree optimization. This flattens the critical path delay. The resulting 16-bit product is sequentially accumulated into an internal 16-bit tracking register on every clock cycle when the clock enable (ena) pin is held high.

## How to test

1. Pulse rst_n low to reset the accumulator register to zero.
2. Drive the active-high clock enable (ena) pin high to start processing.
3. Feed an 8-bit input vector into ui_in. The hardware computes the square of the input vector via the parallel Vedic matrix array and adds the product to the cumulative sum on the rising edge of clk.
4. Read the live 16-bit cumulative result across the output bus simultaneously:
   - The lower 8 bits are read directly from uo_out.
   - The upper 8 bits are read directly from uio_out.
