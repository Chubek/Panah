copy_memory_from_bytewise:
	#define MEMR_DST CABI_AG0
	#define MEMR_SRC CABI_AG1
	#define MEMR_LEN CABI_AG2
	#define READ_REG CLB1_DWD
	#define READ_QWD CLB1_QWD
	#define READ_LOW CLB1_LOW
	#define CNTR_REG CNTR_QWD

	movq MEMR_LEN, CNTR_REG

1:
	movzbl (MEMR_SRC), READ_REG
	movb READ_LOW, (MEMR_DST)
	incq MEMR_SRC
	incq MEMR_DST

	loop 1b


	ret

	#undef MEMR_DST
	#undef MEMR_SRC
	#undef MEMR_LEN
	#undef READ_REG
	#undef READ_QWD
	#undef READ_LOW
	#undef CNTR_REG


clear_memory_qwordwise:
	#define MEMR_PTR CABI_AG0
	#define MEMR_LEN CABI_AG1
	#define CNTR_REG CNTR_QWD
	#define SHFR_NUM $3
	#define NULL_NUM $0
	#define INCR_NUM $8

	shrq SHFR_NUM, MEMR_LEN
	movq MEMR_LEN, CNTR_REG

1:
	movq NULL_NUM, (MEMR_PTR)
	addq INCR_NUM, MEMR_PTR

	loop 1b

	ret

	#undef MEMR_PTR
	#undef MEMR_LEN
	#undef CNTR_REG
	#undef SHFR_NUM
	#undef NULL_NUM
	#undef INCR_NUM


clear_memory_bytewise:
	#define MEMR_PTR CABI_AG0
	#define MEMR_LEN CABI_AG1
	#define CNTR_REG CNTR_QWD
	#define NULL_NUM $0

	movq MEMR_LEN, CNTR_REG

1:
	movb NULL_NUM, (MEMR_PTR)
	incq MEMR_PTR

	loop 1b

	ret

	#undef MEMR_PTR
	#undef MEMR_LEN
	#undef CNTR_REG
	#undef NULL_NUM
	
