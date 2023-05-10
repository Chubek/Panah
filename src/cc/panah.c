#include "headers/cc/types.h"
#include "headers/cc/addr.h"

int main() {
	panah_inetport_t port = 2211;
	panah_inetport_t nbport = addr_inet_port_to_netbyteorder(port);
}	