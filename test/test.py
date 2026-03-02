# SPDX-FileCopyrightText: © 2026 Isabel Walth
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

async def apply_and_check(dut, op, a, b, expected, test_name):
    """Helper: set inputs, wait, check output"""
    dut.ui_in.value  = (op << 6) | (a & 0x1F)   # op in [7:6], a in [4:0]
    dut.uio_in.value = (b & 0x1F)                # b in [4:0]
    await ClockCycles(dut.clk, 1)
    result = dut.uo_out.value
    # mask expected to 8 bits to handle underflow (e.g. 3-4 = 255)
    expected_8bit = expected & 0xFF
    if result == expected_8bit:
        dut._log.info(f"PASS | {test_name}: op={op:02b} a={a} b={b} = {result}")
    else:
        raise AssertionError(f"FAIL | {test_name}: op={op:02b} a={a} b={b} | expected={expected_8bit} got={result}")


@cocotb.test()
async def test_alu(dut):
    dut._log.info("Starting ALU tests")

    # Set up clock
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value    = 1
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    dut.rst_n.value  = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value  = 1
    await ClockCycles(dut.clk, 1)

    # -------------------------
    # ADD tests (op = 0b00)
    # -------------------------
    dut._log.info("--- ADD Tests ---")
    await apply_and_check(dut, 0b00, 3,  4,  7,   "ADD basic")
    await apply_and_check(dut, 0b00, 0,  0,  0,   "ADD zeros")
    await apply_and_check(dut, 0b00, 1,  0,  1,   "ADD by 0")
    await apply_and_check(dut, 0b00, 0,  1,  1,   "ADD 0+1")
    await apply_and_check(dut, 0b00, 15, 15, 30,  "ADD large")
    await apply_and_check(dut, 0b00, 31, 1,  32,  "ADD 5bit overflow into 8bit")

    # -------------------------
    # SUB tests (op = 0b01)
    # -------------------------
    dut._log.info("--- SUB Tests ---")
    await apply_and_check(dut, 0b01, 10, 3,  7,   "SUB basic")
    await apply_and_check(dut, 0b01, 5,  5,  0,   "SUB equal")
    await apply_and_check(dut, 0b01, 0,  0,  0,   "SUB zeros")
    await apply_and_check(dut, 0b01, 1,  0,  1,   "SUB by 0")
    await apply_and_check(dut, 0b01, 31, 31, 0,   "SUB max equal")
    await apply_and_check(dut, 0b01, 3,  4,  -1,  "SUB underflow -> 255")

    # -------------------------
    # AND tests (op = 0b10)
    # -------------------------
    dut._log.info("--- AND Tests ---")
    await apply_and_check(dut, 0b10, 5,  3,  1,   "AND basic")       # 00101 & 00011 = 00001
    await apply_and_check(dut, 0b10, 0,  31, 0,   "AND with 0")
    await apply_and_check(dut, 0b10, 31, 31, 31,  "AND same")
    await apply_and_check(dut, 0b10, 15, 31, 15,  "AND mask")        # 01111 & 11111 = 01111
    await apply_and_check(dut, 0b10, 21, 10, 0,   "AND no overlap")  # 10101 & 01010 = 00000

    # -------------------------
    # OR tests (op = 0b11)
    # -------------------------
    dut._log.info("--- OR Tests ---")
    await apply_and_check(dut, 0b11, 5,  3,  7,   "OR basic")        # 00101 | 00011 = 00111
    await apply_and_check(dut, 0b11, 0,  0,  0,   "OR zeros")
    await apply_and_check(dut, 0b11, 0,  31, 31,  "OR with 0")
    await apply_and_check(dut, 0b11, 31, 31, 31,  "OR same")
    await apply_and_check(dut, 0b11, 21, 10, 31,  "OR all bits")     # 10101 | 01010 = 11111

    dut._log.info("All tests passed!")