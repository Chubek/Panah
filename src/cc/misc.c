#ifndef __INC_MISC_H
#define __INC_MISC_H
#include "misc.h"
#endif

int assert_equal(void statement_a, void statement_b) {
	return statement_a == statement_b;
}

int assert_unequal(void statement_a, void statement_b) {
	return statement_a != statement_b;
}

int assert_nonzero(void statement) {
	return statement != 0;
}

int assert_zero(void statement) {
	return statement == 0;
}