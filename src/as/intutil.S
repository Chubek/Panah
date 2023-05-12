short_from_bytes:
	#define BYTE_LOB DEST_WRD
	#define BYTE_HIB SRCR_LOW
	#define RETR_DWD ACCM_DWD
	#define RETR_LOW ACCM_LOB
	
	movzwl BYTE_LOB, RETR_DWD
	shll $8, RETR_DWD
	movb BYTE_HIB, RETR_LOW

	ret

	#undef BYTE_LOB
	#undef BYTE_HIB
	#undef RETR_DWD
	#undef RETR_REG
	#undef RETR_LOW

int_from_shorts:
	#define WORD_LOW DEST_WRD
	#define WORD_HII SRCR_WRD
	#define RETR_DWD ACCM_DWD
	#define RETR_WRD ACCM_WRD
	#define RETR_REG CABI_RET

	movzwl WORD_HII, RETR_DWD
	shlq $16, RETR_REG
	movw WORD_LOW, RETR_WRD

	ret

	#undef WORD_LOW
	#undef WORD_HII
	#undef RETR_WRD
	#undef RETR_DWD
	#undef RETR_REG
	

long_from_ints:
	#define INTG_LOW DEST_DWD
	#define INTG_HII SRCR_DWD
	#define RETR_DWD ACCM_DWD
	#define RETR_REG ACCM_QWD

	xorq RETR_REG, RETR_REG
	movl INTG_HII, RETR_DWD
	shlq $32, RETR_REG
	movl INTG_LOW, RETR_DWD

	ret

	#undef INTG_LOW
	#undef INTG_HII
	#undef RETR_REG
	#undef RETR_DWD