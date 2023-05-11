resolve_dns_inet:
	#define ADDR_PTR CABI_AG0
	#define DATA_PTR CABI_AG1
	#define RESV_ADR CABI_AG2
	#define READ_QWD CLB1_QWD
	#define READ_DWD CLB1_DWD
	#define READ_WRD CLB1_WRD
	#define READ_LOW CLB1_LOW
	#define TEMP_QWD CLB2_QWD
	#define TEMP_DWD CLB2_DWD
	#define TEMP_WRD CLB2_WRD
	#define TEMP_LOW CLB2_LOW
	#define CNTR_REG CNTR_QWD
	#define ACCM_REG ACCM_QWD
	#define XIDR_WRD ACCM_WRD
	#define RETR_REG CABI_RET
	#define SEED_REG DATA_QWD
	#define SOCK_TMP BASE_QWD
	#define SOCK_RES SYSC_RET
	#define DPTR_TMP CSV1_QWD
	#define RESV_TMP CSV2_QWD

	pushq DPTR_TMP
	pushq RESV_TMP

	xorq ACCM_REG, ACCM_REG
	xorq CNTR_REG, CNTR_REG
	xorq TEMP_QWD, TEMP_QWD
	xorq SEED_REG, SEED_REG

	movq DATA_PTR, DPTR_TMP
	movq RESV_ADR, RESV_TMP

	rdtsc
	RANDOM_USHORT(ACCM_REG, SEED_REG, TEMP_QWD)
	movw XIDR_WRD, (DATA_PTR)
	addq $OFST_WRD, DATA_PTR 
	movw $GLOBVAR_dns_stock_flags, (DATA_PTR)
	addq $OFST_WRD, DATA_PTR 
	movq $GLOBVAR_dns_stock_qsingle, TEMP_QWD
	movq TEMP_QWD, (DATA_PTR)
	addq $OFST_QWD, DATA_PTR
	
	movq $12, CNTR_REG
	movq $13, TEMP_QWD
1:
	movzbl (ADDR_PTR), READ_DWD
	incq ADDR_PTR
	testq READ_QWD, READ_QWD
	jz 3f
	cmpq $GLOBVAR_ascii_period, READ_QWD
	je 2f
	movb READ_LOW, (DATA_PTR, TEMP_QWD)
	incb (DATA_PTR, CNTR_REG)
	incq TEMP_QWD
	jmp 1b

2:
	movq TEMP_QWD, CNTR_REG
	incq TEMP_QWD
	jmp 1b

3:
	SYSCALL_THREE_ARGS(SYSCNR_socket, $GLOBVAR_inet, $GLOBVAR_sock_dgram, $GLOBVAR_proto_default)
	movq SOCK_RES, SOCK_TMP	

	SYSCALL_THREE_ARGS(SYSCNR_connect, SOCK_TMP, RESV_TMP, $GLOBVAR_size_sockaddr_in)

	SYSCALL_THREE_ARGS(SYSCNR_write, SOCK_TMP, DPTR_TMP, $GLOBVAR_dns_datagram_len)

	movq $OFST_QWD, CNTR_REG
	xorq TEMP_QWD, TEMP_QWD
4:
	movq TEMP_QWD, (DPTR_TMP, CNTR_REG)
	loop 4b

	SYSCALL_THREE_ARGS(SYSCNR_read, SOCK_TMP, DPTR_TMP, $GLOBVAR_dns_datagram_len)

	popq RESV_TMP
	popq DPTR_TMP

	ret

	#undef ADDR_PTR
	#undef DATA_PTR
	#undef RESV_ADR
	#undef READ_QWD
	#undef READ_DWD
	#undef READ_WRD
	#undef READ_LOW
	#undef TEMP_QWD
	#undef TEMP_DWD
	#undef TEMP_WRD
	#undef TEMP_LOW
	#undef CNTR_REG
	#undef ACCM_REG
	#undef XIDR_WRD
	#undef RETR_REG
	#undef SEED_REG
	#undef SOCK_TMP
	#undef SOCK_RES
	#undef DPTR_TMP
	#undef RESV_TMP