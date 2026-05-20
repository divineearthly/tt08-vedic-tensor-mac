import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting Divine Earthly Vedic MAC Test Engine...")

    # Start the system test clock at 50MHz (20ns period)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    # --- SYSTEM RESET ACTIVE ---
    dut._log.info("Applying Master Hardware Reset...")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0  # Active-low reset
    
    # Hold reset for 5 full clock cycles
    for _ in range(5):
        await RisingEdge(dut.clk)
        
    dut.rst_n.value = 1  # Release reset
    
    # Let signals stabilize for 2 cycles
    for _ in range(2):
        await RisingEdge(dut.clk)

    # Move to the Falling Edge to safely drive inputs away from the clock boundary
    await FallingEdge(dut.clk)

    # --- TEST CASE 1 ---
    dut._log.info("Executing Test Case 1: Vector Input = 5")
    dut.ui_in.value = 5  # 5 * 5 = 25 (0x0019)
    
    await RisingEdge(dut.clk)   # Clock edge captures input and updates internal registers
    await FallingEdge(dut.clk)  # Wait for falling edge to sample outputs safely
    
    dut._log.info(f"Outputs -> Lower Byte: {dut.uo_out.value.integer}, Upper Byte: {dut.uio_out.value.integer}")
    assert dut.uo_out.value.integer == 25
    assert dut.uio_out.value.integer == 0

    # --- TEST CASE 2 ---
    dut._log.info("Executing Test Case 2: Vector Input = 12")
    dut.ui_in.value = 12  # 12 * 12 = 144 -> Accumulator: 25 + 144 = 169 (0x00A9)
    
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    
    dut._log.info(f"Outputs -> Lower Byte: {dut.uo_out.value.integer}, Upper Byte: {dut.uio_out.value.integer}")
    assert dut.uo_out.value.integer == 169
    assert dut.uio_out.value.integer == 0

    # --- TEST CASE 3 ---
    dut._log.info("Executing Test Case 3: Upper-Byte Overflow Verification")
    dut.ui_in.value = 20  # 20 * 20 = 400 -> Accumulator: 169 + 400 = 569 (0x0239)
    
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    
    dut._log.info(f"Outputs -> Lower Byte: {dut.uo_out.value.integer}, Upper Byte: {dut.uio_out.value.integer}")
    # 569 in hex is 0x0239 -> Upper Byte = 0x02 (2), Lower Byte = 0x39 (57)
    assert dut.uo_out.value.integer == 57
    assert dut.uio_out.value.integer == 2

    dut._log.info("SUCCESS: All structural parallel Vedic mathematical vectors passed validation!")
