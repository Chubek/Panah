resolve_dns_inet:
	#define ADDR_PTR CABI_AG0
	#define DATA_PTR CABI_AG1
	#define RESV_PTR CABI_AG2
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
	#define RETR_LOW ACCM_LOB
	#define RETR_REG CABI_RET
	#define SEED_REG DATA_QWD
	#define SOCK_TMP BASE_QWD
	#define SOCK_RES SYSC_RET
	#define RECV_LEN SYSC_RET
	#define RETR_WRD ACCM_WRD
	#define RETR_DWD ACCM_DWD

	pushq ADDR_PTR
	pushq DATA_PTR
	pushq RESV_PTR

	SYSCALL_THREE_ARGS($SYSCNR_socket, $GLOBVAR_inet, $GLOBVAR_sock_dgram, $GLOBVAR_proto_default)
	movq SOCK_RES, SOCK_TMP

	popq RESV_PTR
	popq DATA_PTR
	popq ADDR_PTR

	pushq DATA_PTR
	pushq SOCK_TMP
	pushq SOCK_TMP
	pushq DATA_PTR
	pushq SOCK_TMP
	pushq DATA_PTR
	pushq SOCK_TMP
	pushq RESV_PTR
	

	rdtsc
	RANDOM_USHORT(ACCM_REG, SEED_REG, TEMP_QWD)
	movw XIDR_WRD, (DATA_PTR)
	addq $2, DATA_PTR
	movb $1, (DATA_PTR)
	addq $3, DATA_PTR
	movb $1, (DATA_PTR)
	addq $7, DATA_PTR

	movq $0, CNTR_REG
	movq $1, TEMP_QWD
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
	addq $2, TEMP_QWD	
	movl $65537, (DATA_PTR, TEMP_QWD)

	popq RESV_PTR
	movq RESV_PTR, TEMP_QWD
	popq SOCK_TMP

	SYSCALL_THREE_ARGS($SYSCNR_connect, SOCK_TMP, TEMP_QWD, $GLOBVAR_size_sockaddr_in)

	popq DATA_PTR
	movq DATA_PTR, TEMP_QWD
	popq SOCK_TMP

	SYSCALL_THREE_ARGS($SYSCNR_write, SOCK_TMP, TEMP_QWD, $GLOBVAR_dns_datagram_len)

	popq DATA_PTR
	movq $OFST_QWD, CNTR_REG
	xorq RETR_REG, RETR_REG
4:
	andq $0, (DATA_PTR, RETR_REG, OFST_QWD)
	incq RETR_REG
	loop 4b

	movq DATA_PTR, TEMP_QWD
	popq SOCK_TMP
	SYSCALL_THREE_ARGS($SYSCNR_read, SOCK_TMP, TEMP_QWD, $GLOBVAR_dns_datagram_len)
 	
	popq SOCK_TMP
 	SYSCALL_ONE_ARGS($SYSCNR_close, SOCK_TMP)	


	popq DATA_PTR
	movzbl 3(DATA_PTR), TEMP_DWD
	andq $15, TEMP_QWD

	testq TEMP_QWD, TEMP_QWD
	jnz 6f

5:
	ret

6:
	xorq RETR_REG, RETR_REG
	movsx TEMP_LOW, RETR_WRD
	negl RETR_DWD
	jmp 5b

	#undef ADDR_PTR
	#undef DATA_PTR
	#undef RESV_PTR
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
	#undef RECV_LEN