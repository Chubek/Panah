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
#ifndef __INC_INTUTILS_H
#define __INC_INTUTILS_H
#include "intutils.h"
#endif
#ifndef __INC_MEMUTILS_H
#define __INC_MEMUTILS_H
#include "memutils.h"
#endif
#ifndef __INC_GLOBVARS_INC
#define __INC_GLOBVARS_INC
#include "globvars.inc"
#endif

panah_nonyield_t parse_dqflags(panah_dqdata_t querydata, panah_dqflags_s *dst) {
	dst->qr = querydata[0] & 128;
	dst->opcode = querydata[0] & 120;
	dst->aa = querydata[0] & 4;
	dst->tc = querydata[0] & 2;
	dst->rd = querydata[0] & 1;
	dst->ra = querydata[1] & 128;
	dst->z = 0;
	dst->rcode = querydata[1] & 15;
}

panah_nonyield_t parse_dqnumbers(panah_dqdata_t querydata, panah_dqnumbers_s *dst) {
	dst->qdcount = short_from_bytes_msb_left(querydata[0], querydata[1]);
	dst->ancount = short_from_bytes_msb_left(querydata[2], querydata[3]);
	dst->nscount = short_from_bytes_msb_left(querydata[4], querydata[5]);
	dst->arcount = short_from_bytes_msb_left(querydata[6], querydata[7]);
}

panah_nonyield_t parse_dqheader(panah_dqdata_t querydata, panah_dqheader_s *dst) {
	dst->queryid = short_from_bytes_msb_left(querydata[0], querydata[1]);
	parse_dqflags(&querydata[2], &dst->queryflags);
	parse_dqnumbers(&querydata[4], &dst->querynumbers);
}

panah_yield_t parse_dqquestion(panah_dqdata_t querydata, panah_dqquestion_s *dst) {
	clear_memory_qwordwise(dst->qname, DNSASCIIZ_LEN);
	char c = '\0';
	int i = 0;
	unsigned char *ptr = querydata;
	while (c = *ptr++) dst->qname[i++] = c;
	i = (ptr - querydata) - 1;
	dst->qtype = short_from_bytes_msb_left(querydata[i++], querydata[i++]);
	dst->qclass = short_from_bytes_msb_left(querydata[i++], querydata[i++]);
	return i;

}

panah_nonyield_t parse_dqrecord(panah_dqdata_t querydata, panah_dqrecord_s *dst) {
	clear_memory_qwordwise(dst->rdata, DNSQRDATA_LEN);
	int i = 0;
	char c = '\0';
	unsigned char *ptr = querydata;
	while (c = *ptr++) dst->rname[i++] = c;
	i = (ptr - querydata) - 1;
	dst->rtype = short_from_bytes_msb_left(querydata[i++], querydata[i++]);
	dst->rclass = short_from_bytes_msb_left(querydata[i++], querydata[i++]);
	dst->ttl = (signed int)int_from_bytes_msb_left(querydata[i++], querydata[i++], querydata[i++], querydata[i++]);
	dst->rdlen = short_from_bytes_msb_left(querydata[i++], querydata[i++]);
	for (int j = 0; j < dst->rdlen; j++) dst->rdata[j] = querydata[i + j];
}

panah_nonyield_t parse_dnsquery(panah_dqdata_t querydata, panah_dnsquery_s *dst) {
	parse_dqheader(querydata, &dst->queryheader);
	int cursor = parse_dqquestion(&querydata[13], &dst->queryquestion);
	parse_dqrecord(&querydata[13 + cursor], &dst->queryrecord);
}

panah_yield_t make_dnsquery_and_get_rdata(panah_dnsaddr_t dnsaddr, panah_dnsresolver_t resolver, panah_inetport_t port, panah_dqtypeclass_t type, panah_dqrdata_t dst) {
	panah_dqdata_t querydata;
	panah_dnsquery_s queryresult;
	panah_sainet_s resolveraddr = new_inet_addr(resolver, port);
	clear_memory_qwordwise(querydata, DNSQQDATA_LEN);
	panah_yield_t resolveresult = resolve_dns_address(dnsaddr, querydata, &resolveraddr, type);
	if (resolveresult < 0) {
		return resolveresult;
	}
	parse_dnsquery(querydata, &queryresult);
	copy_memory_from_bytewise(dst, queryresult.queryrecord.rdata, DNSQRDATA_LEN);
	return 0;
}

panah_yield_t make_dnsquery_and_get_inetaddr(panah_dnsaddr_t dnsaddr, panah_dnsresolver_t resolver, panah_inetport_t port, panah_inetaddr_t *dst) {
	panah_dqrdata_t rdata;
	panah_yield_t resolveresult = make_dnsquery_and_get_rdata(dnsaddr, resolver, port, GLOBVAR_dns_typeclass_inet, rdata);
	if (resolveresult < 0) {
		return resolveresult;
	}
	copy_memory_from_bytewise(dst, rdata, INETADDR4_LEN);
	return 0;
}

panah_yield_t make_dnsquery_and_get_inet6addr(panah_dnsaddr_t dnsaddr, panah_dnsresolver_t resolver, panah_inetport_t port, panah_inet6addr_t *dst) {
	panah_dqrdata_t rdata;
	panah_yield_t resolveresult = make_dnsquery_and_get_rdata(dnsaddr, resolver, port, GLOBVAR_dns_typeclass_inet6, rdata);	
	if (resolveresult < 0) {
		return resolveresult;
	}
	copy_memory_from_bytewise(dst, rdata, INETADDR6_LEN);
	return 0;
}


#if defined ( __TEST__ ) && defined ( __TEST_RESOLVE__ )

int main () {
	panah_inetaddr_t inet;
	panah_inet6addr_t inet6;
	panah_inetaddr_t check;
	asciizhost_to_inetaddr("93.184.216.34", &check);
	make_dnsquery_and_get_inetaddr("example.com", "8.8.8.8", 53, &inet);
	make_dnsquery_and_get_inet6addr("example.com", "8.8.8.8", 53, &inet6);
}

#endif