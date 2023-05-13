#ifndef __INC_TYPE_H
#define __INC_TYPE_H
#include "types.h"
#endif
#ifndef __INC_ADDR_H
#define __INC_ADDR_H
#include "addr.h"
#endif
#ifndef __INC_RESOLVE_H
#define __INC_RESOLVE_H
#include "resolve.h"
#endif
#ifndef __INC_GLOBVARS_INC
#define __INC_GLOBVARS_INC
#include "meta/globvars.inc"
#endif

panah_yield_t parse_dqheader(panah_dqst`atic_t querydata, panah_dqheader_s *dst) {

}
panah_yield_t parse_dqquestion(panah_dqstatic_t querydata, panah_dqquestion_s *dst);
panah_yield_t parse_dqrecord(panah_dqstatic_t querydata, panah_dqrecord_s *dst);
panah_yield_t parse_dnsquery(panah_dqstatic_t querydata, panah_dnsquery_s *dst);
panah_yield_t make_dnsquery_and_get_inetaddr(panah_dnsresolver_t resolver, panah_inetport_t port, panah_inetaddr_t *dst);