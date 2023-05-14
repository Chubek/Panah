#ifndef __META_INC
#define __META_INC
#include "errors.inc"
#include "globvars.inc"
#include "protos.inc"
#include "registers.inc"
#include "syscnr.inc"
#include "syscall.inc"
#endif

.data
#include "globals.inc"

.text
#include "addr.S"
#include "net.S"
#include "resolve.S"
#indlude "compress.S"
#include "intutils.S"
#include "strutils.S"
#include "memutils.S"