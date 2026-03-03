<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a simple ALU with four operations: add, subtract, AND, and OR. It accepts two inputs ui_in and uio_in. The operands are five bits, a is in ui_in [4:0] and b is in uio_in [4:0]. The operation is two bits, stored in ui_in [7:6]. The final result is found using multiplexers, which select the correct output value based on the operator. The eight bit result is stored in uo_out.

## How to test

To use this ALU, set ui_in [7:6] to select the operation, ui_in [4:0] for operand a, and uio_in [4:0] for operand b. Recieve the result from uo_out. The testbench covers the basic and corner functionality of the add, sub, AND, and OR operations. It tests for corner cases for additon, such as: a single zero operand, bit overflow, maximum/minimum sums, and MSB input operands. For subtraction, it tests for equal operands, zero operands, bit underflow, minimum/maximum values, and a single MSB operand. For AND operator, it tests for zero operands, all high bit operands, mask operations (verify partial bit operand), no overlapping bits, MSB for both and one operands. For OR operation, it tests for zero for both and single operands, all high bit operands, complementary operands, MSB for both and single operand. Given operation outputs, it tests the mux tree with set operand values for correctness based on different operation (op) values. It also tests unused bits or noise by setting them high to ensure they do not affect the functionality of the ALU. 

## External hardware

N/A.
