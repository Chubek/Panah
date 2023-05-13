#ifndef __INC_TYPES_H
#define __INC_TYPES_H
#include "types.h"
#endif
#ifndef __INC_STRUTILS_H
#define __INC_STRUTILS_H
#include "strutils.h"
#endif
#ifndef __INC_INTUTILS_H
#define __INC_INTUTILS_H
#include "intutils.h"
#endif
#ifndef __INC_RESOLVE_H
#define __INC_RESOLVE_H
#include "resolve.h"
#endif
#ifndef __INC_ADDR_H
#define __INC_ADDR_H
#include "addr.h"
#endif



#if defined ( __TEST__ ) && defined ( __TEST_INTUTILS__ )

int main() {
	unsigned char b1 = 255;
	unsigned char b2 = 254;
	unsigned char b3 = 127;
	unsigned char b4 = 1;
	unsigned char b5 = 12;
	unsigned char b6 = 45;
	unsigned char b7 = 145;
	unsigned char b8 = 12;

	unsigned short wordbe = short_from_bytes_msb_left(b1, b2);
	unsigned short wordle = short_from_bytes_msb_right(b1, b2);
	unsigned int dwordbe = int_from_bytes_msb_left(b1, b2, b3, b4);
	unsigned int dwordle = int_from_bytes_msb_right(b1, b2, b3, b4);
	unsigned long qwordbe = long_from_bytes_msb_left(b1, b2, b3, b4, b5, b6, b7, b8);
	unsigned long qwordle = long_from_bytes_msb_right(b1, b2, b3, b4, b5, b6, b7, b8);
	unsigned long longd = ascii_to_long("12334");
	panah_asciistatic_t asciinum;
	long_to_ascii(longd, asciinum);
} 

#endif

#ifndef __TEST__
int main() {
}	
#endif