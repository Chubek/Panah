print_asciiz_to_stdout:
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


print_asciiz_to_stderr:
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


reverse_string_nbytes:
	#define STRN_PTR CABI_AG0
	#define STRN_LEN CABI_AG1
	#define CNTR_REG CNTR_QWD
	#define READ_REG ACCM_DWD
	#define READ_LOW ACCM_LOB
	#define READ_QWD ACCM_QWD
	#define TEMP_QWD CLB2_QWD

	movq STRN_LEN, CNTR_REG
	movq STRN_PTR, TEMP_QWD

1:
	movzbl (TEMP_QWD), READ_REG
	incq TEMP_QWD
	pushq READ_QWD
	loop 1b

	movq STRN_LEN, CNTR_REG

2:
	popq READ_QWD
	movb READ_LOW, (STRN_PTR)
	incq STRN_PTR
	loop 2b

	ret

	#undef STRN_PTR
	#undef STRN_LEN
	#undef CNTR_REG
	#undef READ_REG
	#undef READ_LOW
	#undef READ_QWD
	#undef TEMP_QWD
