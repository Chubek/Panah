#ifndef __INC_CC_HEADERS
#define __INC_CC_HEADERS
#include "headers/cc/types.h"
#include "headers/cc/addr.h"
#include "headers/cc/resolve.h"
#endif

int main() {
	panah_sainet_s resolver = addr_new_sainet("8.8.8.8", 53);
	panah_dqstatic_t querydata;
	panah_dnsaddr_t dnsaddr = "google.com";
	panah_yield_t yield = resolve_dns_inet(dnsaddr, querydata, &resolver);
	panah_dnsquery_s response = (panah_dnsquery_s)querydata;
}	