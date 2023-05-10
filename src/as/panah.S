#ifndef __META_INC
#define __META_INC
#include "meta/errors.inc"
#include "meta/globvars.inc"
#include "meta/protos.inc"
#include "meta/registers.inc"
#include "meta/syscnr.inc"
#endif

.data
#include "headers/as/addr.S"
#include "headers/as/net.S"


.text
#include "addr.S"
#include "net.S"
