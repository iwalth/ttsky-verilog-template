<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a simple ALU with four operations: add, subtract, AND, and OR. It accepts two inputs ui_in and uio_in. The operands are five bits, a is in ui_in [4:0] and b is in uio_in [4:0]. The operation is two bits, stored in ui_in [7:6]. The final result is found using multiplexers, which select the correct output value based on the operator. The eight bit result is stored in uo_out.

## How to test

To use this ALU, set ui_in [7:6] to select the operation, ui_in [4:0] for operand a, and uio_in [4:0] for operand b. Recieve the result from uo_out.

## External hardware

N/A.
