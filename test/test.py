import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

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
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1  # Release reset
    await ClockCycles(dut.clk, 2)

    # --- TEST CASE 1 ---
    dut._log.info("Executing Test Case 1: Vector Input = 5")
    # Our core evaluates ui_in * ui_in -> 5 * 5 = 25 (0x0019)
    dut.ui_in.value = 5
    await ClockCycles(dut.clk, 1)
    
    dut._log.info(f"Hardware Outputs Observed -> Lower Byte: {dut.uo_out.value.integer}, Upper Byte: {dut.uio_out.value.integer}")
    assert dut.uo_out.value.integer == 25
    assert dut.uio_out.value.integer == 0

    # --- TEST CASE 2 ---
    dut._log.info("Executing Test Case 2: Vector Input = 12")
    # Our core evaluates 12 * 12 = 144. Cumulative Accumulation: 25 + 144 = 169 (0x00A9)
    dut.ui_in.value = 12
    await ClockCycles(dut.clk, 1)
    
    dut._log.info(f"Hardware Outputs Observed -> Lower Byte: {dut.uo_out.value.integer}, Upper Byte: {dut.uio_out.value.integer}")
    assert dut.uo_out.value.integer == 169
    assert dut.uio_out.value.integer == 0

    # --- TEST CASE 3 ---
    dut._log.info("Executing Test Case 3: Overflow Verification Loop")
    # Forcing accumulation to scale past 8-bit boundaries to test upper-byte streaming
    dut.ui_in.value = 20 # 20 * 20 = 400. Cumulative Accumulation: 169 + 400 = 569 (0x0239)
    await ClockCycles(dut.clk, 1)
    
    dut._log.info(f"Hardware Outputs Observed -> Lower Byte: {dut.uo_out.value.integer}, Upper Byte: {dut.uio_out.value.integer}")
    # 569 in hex is 0x0239 -> Upper Byte = 0x02 (2), Lower Byte = 0x39 (57)
    assert dut.uo_out.value.integer == 57
    assert dut.uio_out.value.integer == 2

    dut._log.info("SUCCESS: All structural parallel Vedic mathematical vectors passed validation!")
