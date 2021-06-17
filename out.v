module rtl_code (a0, a1, a2, a3, a4, a5, a9);

	input a0;
	input a1;
	input a2;
	input a3;
	input a4;
	output a5;
	output a9;

	wire a5;
	wire a6;
	wire a7;
	wire a8;

	assign a5 = a0 & a6;
	assign a6 = a1 | a2;
	assign a7 = a3 & a4;
	assign a8 = a6 & a7;
	assign a9 = ~a8
endmodule