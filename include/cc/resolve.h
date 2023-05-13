extern panah_yield_t resolve_dns_inet(panah_dnsaddr_t dnsaddr, panah_dqstatic_t querydata, panah_sainet_s *resolver);
panah_yield_t parse_dqheader(panah_dqstatic_t querydata, panah_dqheader_s *dst);
panah_yield_t parse_dqquestion(panah_dqstatic_t querydata, panah_dqquestion_s *dst);
panah_yield_t parse_dqrecord(panah_dqstatic_t querydata, panah_dqrecord_s *dst);
panah_yield_t parse_dnsquery(panah_dqstatic_t querydata, panah_dnsquery_s *dst);
panah_yield_t make_dnsquery_and_get_inetaddr(panah_dnsresolver_t resolver, panah_inetport_t port, panah_inetaddr_t *dst);