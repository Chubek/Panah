#ifdef __SYMBLDICT_LEN__
#define SYMBLDICT_LEN __SYMBLDICT_LEN__
#else
#define SYMBLDICT_LEN 65535
#endif
#ifdef __DNSQRDATA_LEN__
#define DNSQRDATA_LEN __DNSQRDATA_LEN__
#else
#define DNSQRDATA_LEN 64
#endif
#ifdef __DNSASCIIZ_LEN__
#define DNSASCIIZ_LEN __DNSASCIIZ_LEN__
#else
#define DNSASCIIZ_LEN 256
#endif
#ifdef __NUMASCIIZ_LEN__
#define NUMASCIIZ_LEN __NUMASCIIZ_LEN__
#else
#define NUMASCIIZ_LEN 21
#endif
#ifdef __DNSQQDATA_LEN__
#define DNSQQDATA_LEN __DNSQQDATA_LEN__
#else
#define DNSQQDATA_LEN 512
#endif
#define INETADDR6_LEN 16
#define INETADDR4_LEN 4


typedef void *memaddr_t;
typedef void nonyield_t;
typedef signed char domainz_t[DNSASCIIZ_LEN];
typedef signed char dqrdata_t[DNSQRDATA_LEN];
typedef signed char *asciizinet_t;
typedef signed char *asciinum_t;
typedef signed char *dnsaddr_t;
typedef signed char *asziiz_t;
typedef signed char *dnsresolver_t;
typedef signed int dnsttl_t;
typedef signed int yield_t;
typedef signed char asciiznum_t[NUMASCIIZ_LEN];
typedef unsigned char symbldict_t[SYMBLDICT_LEN];
typedef unsigned char dqdata_t[DNSQQDATA_LEN];
typedef unsigned char ptsymbol_t;
typedef unsigned int inetaddr_t;
typedef unsigned int dqtypeclass_t;
typedef unsigned short inetport_t;
typedef unsigned short dqxid_t;
typedef unsigned short dqflag_t;
typedef unsigned short dqnumber_t;
typedef unsigned long inet6addr_t[2];
typedef unsigned short dqflag_t;
typedef unsigned short dqtype_t;
typedef unsigned short dqclass_t;
typedef unsigned short dqlen_t;
typedef unsigned short safamily_t;
typedef unsigned long memsize_t;
typedef unsigned long strlen_t;
typedef unsigned long ptparent_t;
typedef unsigned long ptindex_t;

typedef struct PanahDNSQueryFlags {
	dqflag_t qr;
	dqflag_t opcode;
	dqflag_t aa;
	dqflag_t tc;
	dqflag_t rd;
	dqflag_t ra;
	dqflag_t z;
	dqflag_t rcode;
} dqflags_s;

typedef struct PanahDNSQueryNumbers {
	dqnumber_t qdcount;
	dqnumber_t ancount;
	dqnumber_t nscount;
	dqnumber_t arcount;
} dqnumbers_s;

typedef struct PanahDNSQueryHeader {
	dqxid_t queryid;
	dqflags_s queryflags;
	dqnumbers_s querynumbers;
} dqheader_s;

typedef struct PanahDNSQueryQuestion {
	domainz_t qname;
	dqtype_t qtype;
	dqclass_t qclass;
} dqquestion_s;

typedef struct PanahDNSQueryResourceRecord {
	domainz_t rname;
	dqtype_t rtype;
	dqclass_t rclass;
	dnsttl_t ttl;
	dqlen_t rdlen;
	dqrdata_t rdata; 
} dqrecord_s;

typedef struct PanahDNSQuery {
	dqheader_s queryheader;
	dqquestion_s queryquestion;
	dqrecord_s queryrecord;
} dnsquery_s;

typedef struct PanahINETAddress {
    inetaddr_t s_addr;
} inetaddr_s;

typedef struct SocketAddressInet {
	safamily_t sin_family;
	inetport_t sin_port;
	inetaddr_s sin_addr;
	unsigned char pad[8];
} sainet_s;

typedef struct PrefixTreeItem {
	ptparent_t parentidx;
	ptindex_t selfidx;
	ptsymbol_t symbol;
} prefixtree_s;

typedef struct SymbolDictionary {
	symbldict_t storage;
	prefixtree_s prefixes[SYMBLDICT_LEN];
} symbldict_s;