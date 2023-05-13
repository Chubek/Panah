// Part of Panah Packet Wrangler: https://github.com/Chubek/Panah
// Released under MIT License, see Panah/LICENSE for more info


/*
* the following subroutine makes a dns query based on type
* it accepts a dns address as a null-terminated string
* the second argument is a 512-byte array, it can be both statically or dynamically allocated
* the third argument is the resolver inetaddr_in struct, must have size of 16 bytes
* the forth argument is a the type, but it should also contain the class as the last two bytes, which is a 2-byte x00x001 (internet)
* for better details of how a dns request works see scripts/dnsrezulf.py
*/

resolve_dns_address:
	#define ADDR_PTR CABI_AG0
	#define DATA_PTR CABI_AG1
	#define RESV_PTR CABI_AG2
	#define TYPE_NUM CABI_AG3
	#define TNUM_DWD CNTR_DWD
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

	pushq ADDR_PTR    					/* we push the arguments to stack because we wish to make a syscall */
	pushq DATA_PTR
	pushq RESV_PTR
	pushq TYPE_NUM
										/* we open a socket, of ipv4 family, and datagram type (udp)	    */
	SYSCALL_THREE_ARGS($SYSCNR_socket, $GLOBVAR_inet, $GLOBVAR_sock_dgram, $GLOBVAR_proto_default)	
	movq SOCK_RES, SOCK_TMP				/* after socket syscall, we save the socket to temp register	    */

	popq TYPE_NUM						/* pop back all the saved registers, in reverse order 			    */ 
	popq RESV_PTR
	popq DATA_PTR
	popq ADDR_PTR

	pushq DATA_PTR						/* push the values we need to the stack for future use				*/
	pushq SOCK_TMP						/* we will pop these values back and read them in the process		*/
	pushq SOCK_TMP
	pushq DATA_PTR
	pushq SOCK_TMP
	pushq DATA_PTR
	pushq SOCK_TMP
	pushq RESV_PTR
	pushq TYPE_NUM
	

	rdtsc								/* generate the xid for our dns query, see scripts/dnsrezulf.py		*/
	RANDOM_USHORT(ACCM_REG, SEED_REG, TEMP_QWD)
	movw XIDR_WRD, (DATA_PTR)
	addq $2, DATA_PTR					/*  add the header, it just says we want recursion				    */
	movb $1, (DATA_PTR)
	addq $3, DATA_PTR
	movb $1, (DATA_PTR)					/* add the number of questions (1)									*/
	addq $7, DATA_PTR	

	movq $0, CNTR_REG
	movq $1, TEMP_QWD
1:										/* the following loop reads the dns address into our query		     */
	movzbl (ADDR_PTR), READ_DWD			/* again, dnsrezulf.py has better descriptions						 */
	incq ADDR_PTR
	testq READ_QWD, READ_QWD			/* check if we got a null, or a period (ascii 46), react accordingly */
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
	addq $2, TEMP_QWD					/* we add the class for internet and type for record type			 */
	popq TYPE_NUM
	movl TNUM_DWD, (DATA_PTR, TEMP_QWD)

	popq RESV_PTR
	movq RESV_PTR, TEMP_QWD
	popq SOCK_TMP
										  /* make a connect syscall with our given GLOBVAR_size_sockaddr_in	 */
	SYSCALL_THREE_ARGS($SYSCNR_connect, SOCK_TMP, TEMP_QWD, $GLOBVAR_size_sockaddr_in)

	popq DATA_PTR
	movq DATA_PTR, TEMP_QWD
	popq SOCK_TMP
										  /* send our query													 */
	SYSCALL_THREE_ARGS($SYSCNR_write, SOCK_TMP, TEMP_QWD, $GLOBVAR_dns_datagram_len)

	popq DATA_PTR
	movq $OFST_QWD, CNTR_REG
	xorq RETR_REG, RETR_REG
4:										  /* this loop will clear our data for reading back					 */
	andq $0, (DATA_PTR, RETR_REG, OFST_QWD)
	incq RETR_REG
	loop 4b

	movq DATA_PTR, TEMP_QWD
	popq SOCK_TMP						 /* read results back													*/
	SYSCALL_THREE_ARGS($SYSCNR_read, SOCK_TMP, TEMP_QWD, $GLOBVAR_dns_datagram_len)
 	
	popq SOCK_TMP						/* close the socket because we do no longer need it 					*/
 	SYSCALL_ONE_ARGS($SYSCNR_close, SOCK_TMP)	


	popq DATA_PTR
	movzbl 3(DATA_PTR), TEMP_DWD
	andq $15, TEMP_QWD					/* read the rcode of response, to see whether it is errenous or not		*/

	testq TEMP_QWD, TEMP_QWD
	jnz 6f

5:										/* at this point the data has been read back, next is up to the caller	*/
	ret

6:
	xorq RETR_REG, RETR_REG
	movsx TEMP_LOW, RETR_WRD
	negl RETR_DWD						/* if rcode != 0, we two-complement the result and return it 			*/
	jmp 5b

	#undef ADDR_PTR
	#undef DATA_PTR
	#undef RESV_PTR
	#undef TYPE_NUM
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
	#undef RECV_LEN
	#undef RETR_WRD
	#undef RETR_DWD
	#undef RETR_LOW 
	#undef RETR_REG