print_nullterm_string_to_stdout:
	#define ADDR_STR CABI_AG0
	#define READ_REG CLB1_DWD
	#define READ_QWD CLB1_QWD
	#define CNTR_REG CNTR_QWD

	xorq CNTR_REG, CNTR_REG

1:
	movzbl (ADDR_STR, CNTR_REG), READ_REG
	incq CNTR_REG
	testq READ_QWD, READ_QWD
	jz 2f
	jmp 1b

2:
	movq ADDR_STR, READ_QWD
	SYSCALL_THREE_ARGS($SYSCNR_write, $GLOBVAR_stdout, READ_QWD, CNTR_REG)
	ret

	#undef ADDR_STR
	#undef READ_REG
	#undef READ_QWD
	#undef CNTR_REG


print_nullterm_string_to_stderr:
	#define ADDR_STR CABI_AG0
	#define READ_REG CLB1_DWD
	#define READ_QWD CLB1_QWD
	#define CNTR_REG CNTR_QWD

	xorq CNTR_REG, CNTR_REG

1:
	movzbl (ADDR_STR, CNTR_REG), READ_REG
	incq CNTR_REG
	testq READ_QWD, READ_QWD
	jz 2f
	jmp 1b

2:
	movq ADDR_STR, READ_QWD
	SYSCALL_THREE_ARGS($SYSCNR_write, $GLOBVAR_stderr, READ_QWD, CNTR_REG)
	ret

	#undef ADDR_STR
	#undef READ_REG
	#undef READ_QWD
	#undef CNTR_REG
