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
	signed char str[11] =  {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\0'};
	reverse_string_nbytes(str, 10);
}

#endif