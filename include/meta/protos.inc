/*  multiplication achieved by shifting left 3 and 1 times  */
#define MULT_BY_TEN_QUAD(reg, temp) 	\
	movq reg, temp;						\
	shlq $3, reg;						\
	shlq $1, temp;						\
	addq temp, reg;
	
/*  a lineader congruational generator, mod 65536 */
/*  mult is 33, no increment, basically the djb2 magic  */
#define RANDOM_USHORT(accumulator, seed, temp)		\
	movq seed, accumulator;							\
	movq seed, temp; 								\
	shlq $5, accumulator;							\
	addq temp, accumulator;							\
	movq accumulator, temp;							\
	shrq $16, temp;									\
	shlq $16, temp;									\
	subq temp, accumulator;
