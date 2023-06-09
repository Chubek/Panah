/*
* the following converts a null-terminated IPV4 address into a 32-bit unsigned integer
* the address is given at argument 0, and the destination at argument 1
* the destination must be a pointer to memory, 4 bytes in length
* it can be allocated both statically and dynamically, however, I recommend just passing it pointer to an int
*/
asciizhost_to_inetaddr:
	#define ADDR_PTR CABI_AG0
	#define INGT_PTR CABI_AG1
	#define SHFL_CNT CNTR_QWD
	#define TEMP_QWD CLB1_QWD
	#define TEMP_DWD CLB1_DWD
	#define READ_QWD CLB2_QWD
	#define READ_DWD CLB2_DWD
	#define READ_LOW CLB2_LOW
	#define RESL_REG ACCM_QWD
	#define COMP_RES $-2
	#define NULL_RES $-48

	xorq RESL_REG, RESL_REG
	xorq SHFL_CNT, SHFL_CNT
	xorq TEMP_QWD, TEMP_QWD
	movl TEMP_DWD, (INGT_PTR)

1:												/*  this is our atoi branch                                     */
	movzbl (ADDR_PTR), READ_DWD  				/*  read byte   												*/
	incq ADDR_PTR								/*  increase pointer 											*/
	cmpq $GLOBVAR_ascii_nine, READ_QWD			/*  larger than ascii for 9?                                    */
	jg 4f
	subq $GLOBVAR_ascii_zero, READ_QWD          /*  it is maybe period or null  								*/ 
	js 2f										/*  if it is either, the sign flag will be set                  */


	MULT_BY_TEN_QUAD(RESL_REG, TEMP_QWD)        /*   multiply by ten, see the prototype   						*/
	addq READ_QWD, RESL_REG                 
	jmp 1b                                      /*   loop back to reading digits   								*/

2:                                              /*   this is our host-to-inet branch 							*/           
	testq $GLOBVAR_upper_u16, RESL_REG			/*   is our current byte not a byte? 							*/
	jnz 5f										/*   we are checking whether our atoi has converted  > 255 		*/

	shlq SHFL_CNT, RESL_REG 					/*   shift left, netbyteorder is msb-first (big endian) 		*/

	movq $GLOBVAR_upper_u64, TEMP_QWD
	testq TEMP_QWD, RESL_REG		            /*   are we having more than 32 bits?  							*/
	jnz 6f

	addq $OFST_QWD, SHFL_CNT					/*   add 8 to shift num   										*/          
	orq RESL_REG, (INGT_PTR)                    /*   bitwise-or the result with the final pointer  				*/

	cmpq NULL_RES, READ_QWD	                    /*   null reached? String must be null-terminated 				*/
	je 3f										/*   notice that, READ_QWD must now hold -48 if it was null 	*/

	cmpq COMP_RES, READ_QWD				        /*    if not null, was our seperator period?  					*/
	jne 4f										/*    notice that, READ_QWD must now hold -2 if it was period 	*/

	xorq RESL_REG, RESL_REG						/*    zero out accumulator for the next atoi					*/
	jmp 1b                                      /*    loop back to our atoi branch   							*/

3:                                              /*    our return branch  										*/
	ret

4:
	movq $ENONONDIGITALLOWED, RESL_REG           /*   unallowed digit error, termination 						*/
	jmp 3b

5:
	movq $ENONBYTEINET, RESL_REG                 /*   non-byte number, terminated 								*/
	jmp 3b

6:
	movq $EINETADDRTOOLONG, RESL_REG             /*   address too long, terminated 								*/
	jmp 3b


	#undef ADDR_PTR
	#undef INGT_PTR
	#undef SHFL_CNT
	#undef TEMP_QWD
	#undef TEMP_DWD
	#undef READ_QWD
	#undef READ_DWD
	#undef READ_LOW
	#undef RESL_REG
	#undef COMP_RES
	#undef NULL_RES


/*
* the following converts a short integer to net byte orderm aka big endian
* the result is returned in the accumulator
*/
cshort_port_to_netorder:
	#define PORT_REG CABI_AG0
	#define RESL_REG CABI_RET
	#define RESL_HIB ACCM_HIB
	#define RESL_LOB ACCM_LOB


	movq PORT_REG, RESL_REG						/*   move argument to accumulator                                */
	xchgb RESL_HIB, RESL_LOB					/*   exchange lower bits of accumulator with higher              */
												/*   en effet this will make it MSB, ipso facto net-compiant     */
	ret

	#undef PORT_REG
	#undef RESL_REG
	#undef RESL_HIB
	#undef RESL_LOB

