/*
 * Copyright (c) 2026 Isabel Walth
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_ALU (
    input  wire [7:0] ui_in,    // [7:6] = op, [4:0] = a
    output wire [7:0] uo_out,   // result
    input  wire [7:0] uio_in,   // [4:0] = b
    output wire [7:0] uio_out,  // unused
    output wire [7:0] uio_oe,   // unused
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  wire [4:0] a, b;
  wire [1:0] op;
  assign a = ui_in[4:0];
  assign b = uio_in[4:0];
  assign op = ui_in[7:6];

  wire [7:0] add, sub, And, Or;
  assign add = a + b;
  assign sub = a - b;
  assign And = a & b;
  assign Or  = a | b;

  wire [7:0] mux1_out, mux2_out;

  mux8bit mux1 (.a_i(add), .b_i(sub), .ld_i(op[0]), .y_o(mux1_out));
  mux8bit mux2 (.a_i(And), .b_i(Or), .ld_i(op[0]), .y_o(mux2_out));

  wire [7:0] mux3_o;
  assign uo_out = mux3_o;
  mux8bit mux3 (.a_i(mux1_out), .b_i(mux2_out), .ld_i(op[1]), .y_o(mux3_o));

  // All output pins must be assigned. If not used, assign to 0.
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ui_in[5], uio_in[7:5], ena, clk, rst_n, 1'b0};

endmodule

module mux8bit(
    input  [7:0] a_i,
    input  [7:0] b_i,
    input        ld_i,
    output [7:0] y_o
);
    assign y_o = ({8{~ld_i}} & a_i) | ({8{ld_i}} & b_i);
endmodule