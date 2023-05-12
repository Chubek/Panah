#ifndef __INC_CC_HEADERS
#define __INC_CC_HEADERS
#include "headers/cc/types.h"
#include "headers/cc/addr.h"
#include "headers/cc/resolve.h"
#endif

panah_yield_t parse_dqheader(panah_dqstatic_t querydata, panah_dqheader_s *dst) {
	
}
panah_yield_t parse_dqquestion(panah_dqstatic_t querydata, panah_dqquestion_s *dst);
panah_yield_t parse_dqrecord(panah_dqstatic_t querydata, panah_dqrecord_s *dst);
panah_yield_t parse_dnsquery(panah_dqstatic_t querydata, panah_dnsquery_s *dst);
panah_yield_t make_dnsquery_and_get_inetaddr(panah_dnsresolver_t resolver, panah_inetport_t port, panah_inetaddr_t *dst);