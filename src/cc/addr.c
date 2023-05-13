#ifndef __INC_TYPE_H
#define __INC_TYPE_H
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


panah_sainet_s addr_new_sainet(panah_hostaddr_t host, panah_inetport_t port) {
	panah_inetaddr_t addr = 0;
	addr_inet_address_to_netbyteorder(host, &addr);

	return (panah_sainet_s){
		.sin_family = GLOBVAR_inet,
		.sin_port = addr_inet_port_to_netbyteorder(port),
		.sin_addr = addr, 
	};
}