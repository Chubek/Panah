#define MULT_BY_TEN_QUAD(reg, temp) 	\
	movq reg, temp;						\
	shlq $3, reg;						\
	shlq $1, temp;						\
	addq temp, reg;
	