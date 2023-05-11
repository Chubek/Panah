#define SYSCALL_ZERO_ARGS(nr) 		  						\
	movq nrr, SYSC_NRR;										\
	syscall;


#define SYSCALL_ONE_ARGS(nrr, ag0)           				\
	movq nrr, SYSC_NRR;										\
	movq ag0, SYSC_AG0;										\
	syscall;


#define SYSCALL_TWO_ARGS(nrr, ag0, ag1) 					\
	movq nrr, SYSC_NRR;										\
	movq ag0, SYSC_AG0;										\
	movq ag1, SYSC_AG1;										\
	syscall;

#define SYSCALL_THREE_ARGS(nrr, ag0, ag1, ag2)				\
	movq nrr, SYSC_NRR;										\
	movq ag0, SYSC_AG0;										\
	movq ag1, SYSC_AG1;										\
	movq ag2, SYSC_AG2;										\
	syscall;


#define SYSCALL_FOUR_ARGS(nrr, ag0, ag1, ag2, ag3)			\
	movq nrr, SYSC_NRR;										\
	movq ag0, SYSC_AG0;										\
	movq ag1, SYSC_AG1;										\
	movq ag2, SYSC_AG2;										\
	movq ag3, SYSC_AG3;										\
	syscall;


#define SYSCALL_FIVE_ARGS(nrr, ag0, ag1, ag2, ag3, ag4)		\
	movq nrr, SYSC_NRR;										\
	movq ag0, SYSC_AG0;										\
	movq ag1, SYSC_AG1;										\
	movq ag2, SYSC_AG2;										\
	movq ag3, SYSC_AG3;										\
	movq ag4, SYSC_AG4;										\
	syscall;


#define SYSCALL_SIX_ARGS(nrr, ag0, ag1, ag2, ag3, ag4, ag5)	\
	movq nrr, SYSC_NRR;										\
	movq ag0, SYSC_AG0;										\
	movq ag1, SYSC_AG1;										\
	movq ag2, SYSC_AG2;										\
	movq ag3, SYSC_AG3;										\
	movq ag4, SYSC_AG4;										\
	movq ag5, SYSC_AG5;										\
	syscall;
