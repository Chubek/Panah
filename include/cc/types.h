typedef void panah_nonyield_t;
typedef signed char *panah_hostaddr_t;
typedef signed char *panah_dqdata_t;
typedef signed char *panah_asciinum_t;
typedef signed char *panah_dnsaddr_t;
typedef signed char *panah_dqname_t;
typedef signed char *panah_asziiz_t;
typedef signed char *panah_dnsresolver_t;
typedef signed int panah_dnsttl_t;
typedef signed int panah_yield_t;
typedef signed char panah_asciiznum_t[21];
typedef unsigned char panah_dqdata_t[512];
typedef unsigned int panah_inetaddr_t;
typedef unsigned int panah_dqtype_t;
typedef unsigned short panah_inetport_t;
typedef unsigned short panah_dqxid_t;
typedef unsigned short panah_dqflag_t;
typedef unsigned short panah_dqnumber_t;
typedef unsigned long panah_inet6addr_t[2];
typedef unsigned short panah_dqflag_t;
typedef unsigned short panah_dqtype_t;
typedef unsigned short panah_dqclass_t;
typedef unsigned short panah_dqlen_t;
typedef unsigned short panah_safamily_t;


typedef struct PanahDNSQueryFlags {
	panah_dqflag_t qr;
	panah_dqflag_t opcode;
	panah_dqflag_t aa;
	panah_dqflag_t tc;
	panah_dqflag_t rd;
	panah_dqflag_t ra;
	panah_dqflag_t z;
	panah_dqflag_t rcode;
} panah_dqflags_s;

typedef struct PanahDNSQueryNumbers {
	panah_dqnumber_t qdcount;
	panah_dqnumber_t ancount;
	panah_dqnumber_t nscount;
	panah_dqnumber_t arcount;
} panah_dqnumbers_s;

typedef struct PanahDNSQueryHeader {
	panah_dqxid_t queryid;
	panah_dqflags_s queryflags;
	panah_dqnumbers_s querynumbers;
} panah_dqheader_s;

typedef struct PanahDNSQueryQuestion {
	panah_dqname_t qname;
	panah_dqtype_t qtype;
	panah_dqclass_t qclass;
} panah_dqquestion_s;

typedef struct PanahDNSQueryResourceRecord {
	panah_dqname_t rname;
	panah_dqtype_t rtype;
	panah_dqclass_t rclass;
	panah_dnsttl_t ttl;
	panah_dqlen_t rdlen;
	panah_dqdata_t rdata; 
} panah_dqrecord_s;

typedef struct PanahDNSQuery {
	panah_dqheader_s qheader;
	panah_dqquestion_s qquestion;
	panah_dqrecord_s qrecord;
} panah_dnsquery_s;

typedef struct PanahINETAddress {
    panah_inetaddr_t s_addr;
} panah_inetaddr_s;


typedef struct SocketAddressInet {
	panah_safamily_t sin_family;
	panah_inetport_t sin_port;
	panah_inetaddr_s sin_addr;
	unsigned char pad[8];
} panah_sainet_s;