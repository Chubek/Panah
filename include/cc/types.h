typedef void panah_nonyield_t;
typedef signed char *panah_hostaddr_t;
typedef signed char *panah_dqdata_t;
typedef signed char *panah_asciinum_t;
typedef signed char *panah_dnsaddr_t;
typedef signed char *panah_dqname_t;
typedef signed char *panah_nulltstr_t;
typedef signed char *panah_dnsresolver_t;
typedef signed int panah_dnsttl_t;
typedef signed int panah_yield_t;
typedef signed char panah_asciistatic_t[21];
typedef unsigned char panah_dqstatic_t[512];
typedef unsigned int panah_inetaddr_t;
typedef unsigned short panah_inetport_t;
typedef unsigned short panah_dqxid_t;
typedef unsigned short panah_dqflag_t;
typedef unsigned long panah_dqnumbers_t;
typedef unsigned short panah_dqtype_t;
typedef unsigned short panah_dqclass_t;
typedef unsigned short panah_dqlen_t;
typedef unsigned short panah_safamily_t;

typedef struct PanahdqHeader {
	panah_dqxid_t queryid;
	panah_dqflag_t queryflags;
	panah_dqnumbers_t querynumbers;
} panah_dqheader_s;

typedef struct PanahdqQuestion {
	panah_dqname_t dqname;
	panah_dqtype_t dqtype;
	panah_dqclass_t dqclass;
} panah_dqquestion_s;

typedef struct PanahdqResourceRecord {
	panah_dqname_t rname;
	panah_dqtype_t rtype;
	panah_dqclass_t rclass;
	panah_dnsttl_t ttl;
	panah_dqdata_t rdata; 
} panah_dqrecord_s;

typedef struct PanahDNSQuery {
	panah_dqheader_s header;
	panah_dqquestion_s question;
	panah_dqrecord_s record;
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