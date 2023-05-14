#ifndef __INC_TYPES_H
#define __INC_TYPES_H
#include "types.h"
#endif
#ifndef __INC_STRUTILS_H
#define __INC_STRUTILS_H
#include "strutils.h"
#endif


#if defined ( __TEST__ ) && defined ( __TEST_STRUTILS__ )

int main() {
	asciiz_t str = "0123456789";
	reverse_string_nbyte(str, 10);
}

#endif