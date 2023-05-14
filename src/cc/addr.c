#ifndef __INC_TYPES_H
#define __INC_TYPES_H
#include "types.h"
#endif
#ifndef __INC_ADDR_H
#define __INC_ADDR_H
#include "addr.h"
#endif
#ifndef __INC_GLOBVARS_INC
#define __INC_GLOBVARS_INC
#include "globvars.inc"
#endif


sainet_s new_inet_addr(asciizinet_t host, inetport_t port) {
	inetaddr_t addr = 0;
	asciizhost_to_inetaddr(host, &addr);

	return (sainet_s){
		.sin_family = GLOBVAR_inet,
		.sin_port = cshort_port_to_netorder(port),
		.sin_addr = addr, 
	};
}