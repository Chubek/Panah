#ifndef __INC_INTUTILS_H
#define __INC_INTUTILS_H
#include "intutils.h"
#endif
#ifndef __INC_MISC_H
#define __INC_MISC_H
#include "misc.h"
#endif
#ifndef __INC_GLOBVARS_INC
#define __INC_GLOBVARS_INC
#include "globvars.inc"
#endif


unsigned int int_from_bytes(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char msb) {
	unsigned short lsw = short_from_bytes(lsb, byte1);
	unsigned short msw = short_from_bytes(byte2, msb);
	return int_from_shorts(lsw, msw);
}

unsigned long long_from_bytes(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char byte3, unsigned char byte4, unsigned char byte5, unsigned char byte6, unsigned char msb) {
	unsigned short lsd = int_from_bytes(lsb, byte1, byte2, byte3);
	unsigned short msd = int_from_bytes(byte4, byte5, byte6, msb);
	return long_from_ints(lsd, msd);
}

unsigned long ascii_to_long(panah_asciinum_t number) {
	unsigned long number = 0;
	char digit = '\0';
	while (digit = *(number)++) {
		number = ((number << 3) + (number << 1)) + (GLOBVAR_ascii_zero - digit);
	}
	return number;
}
panah_nonyield_t long_to_ascii(unsigned long number, panah_asciistatic_t asciinum) {
	int i = 20;
	unsigned long digit = 0;
	while (number) {
		digit = number % 10;
		asciinum[i--] = GLOBVAR_ascii_zero + digit;
		number /= 10;
	}
}

#if defined (__TEST__) && defined (__TEST_INTUTILS__)

int main() {
	int 
} 

#endif