#ifndef __INC_CC_HEADERS
#define __INC_CC_HEADERS
#include "types.h"
#include "addr.h"
#include "resolve.h"
#include "intutils.h"
#endif

int main() {
	unsigned short s = short_from_bytes(255, 12);
	unsigned int i = int_from_shorts(65535, 1000);
	unsigned long l = long_from_ints(429496721, 11124); 
}	