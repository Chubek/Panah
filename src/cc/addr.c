#ifndef __INC_CC_HEADERS
#define __INC_CC_HEADERS
#include "headers/cc/types.h"
#include "headers/cc/addr.h"
#include "headers/cc/resolve.h"
#include "meta/globvars.inc"
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