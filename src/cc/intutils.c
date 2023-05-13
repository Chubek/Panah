#ifndef __INC_TYPE_H
#define __INC_TYPE_H
#include "types.h"
#endif
#ifndef __INC_INTUTILS_H
#define __INC_INTUTILS_H
#include "intutils.h"
#endif
#ifndef __INC_STRUTILS_H
#define __INC_STRUTILS_H
#include "strutils.h"
#endif
#ifndef __INC_GLOBVARS_INC
#define __INC_GLOBVARS_INC
#include "globvars.inc"
#endif

unsigned short short_from_bytes_msb_left(unsigned char lsb, unsigned char msb) {
	return short_from_bytes(msb, lsb);
}

unsigned short short_from_bytes_msb_right(unsigned char lsb, unsigned char msb) {
	return short_from_bytes(lsb, msb);
}

unsigned int int_from_bytes_msb_left(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char msb) {
	unsigned short lsw = short_from_bytes_msb_left(lsb, byte1);
	unsigned short msw = short_from_bytes_msb_left(byte2, msb);
	return int_from_shorts(lsw, msw);
}

unsigned int int_from_bytes_msb_right(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char msb) {
	unsigned short lsw = short_from_bytes_msb_right(lsb, byte1);
	unsigned short msw = short_from_bytes_msb_right(byte2, msb);
	return int_from_shorts(msw, lsw);
}

unsigned long long_from_bytes_msb_left(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char byte3, unsigned char byte4, unsigned char byte5, unsigned char byte6, unsigned char msb) {
	unsigned int lsd = int_from_bytes_msb_left(lsb, byte1, byte2, byte3);
	unsigned int msd = int_from_bytes_msb_left(byte4, byte5, byte6, msb);
	return long_from_ints(lsd, msd);
}

unsigned long long_from_bytes_msb_right(unsigned char lsb, unsigned char byte1, unsigned char byte2, unsigned char byte3, unsigned char byte4, unsigned char byte5, unsigned char byte6, unsigned char msb) {
	unsigned int lsd = int_from_bytes_msb_right(lsb, byte1, byte2, byte3);
	unsigned int msd = int_from_bytes_msb_right(byte4, byte5, byte6, msb);
	return long_from_ints(msd, lsd);
}

unsigned long ascii_to_long(panah_asciinum_t ascii) {
	unsigned long number = 0;
	char digit = '\0';
	while (digit = *ascii++) {
		number = ((number << 3) + (number << 1)) + (digit - GLOBVAR_ascii_zero);
	}
	return number;
}
panah_nonyield_t long_to_ascii(unsigned long number, panah_asciiznum_t asciinum) {
	int i = 0;
	unsigned long numcopy = number;
	while (numcopy /= 10) i++;
	unsigned char digit = 0;
	while (number) {
		digit = number % 10;
		asciinum[i--] = GLOBVAR_ascii_zero + digit;
		number /= 10;
	}
}
