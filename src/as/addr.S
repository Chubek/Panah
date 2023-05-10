addr_inet_address_to_netbyteorder:
	#define ADDR_PTR CABI_AG0
	#define FRAM_PTR FPPT_QWD
	#define STCK_PTR STPT_QWD
	#define CNTR_REG CNTR_QWD
	#define TEMP_QWD CLB1_QWD
	#define TEMP_DWD CLB1_DWD
	#define TEMP_LOW CLB1_LOW
	#define READ_QWD CLB2_QWD
	#define READ_DWD CLB2_DWD
	#define READ_LOW CLB2_LOW
	#define RESL_REG ACCM_QWD

	xorq RESL_REG, RESL_REG
1:
	movzbl (ADDR_PTR), READ_DWD
	cmpq GLOBVAR_ascii_nine, READ_QWD
	jg 4f
	testq READ_QWD, READ_QWD
	jz 3f
	subq GLOBVAR_ascii_zero, READ_QWD
	js 2f

	MULT_BY_TEN_QUAD(RESL_REG, TEMP_QWD)
	addq READ_QWD, RESL_REG
	jmp 1b