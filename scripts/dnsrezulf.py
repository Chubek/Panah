# Part of Panah Packet Wrangler: https://github.com/Chubek/Panah
# Released under MIT License, see Panah/LICENSE for more info

# this script contain a simple, limited implementation of the
# DNS query system in Python as a part of Panah application
# notice that this script is not a complete implementation 
# and has only been written for prototyping Panah DNS resolver
# please only use for educational/prototyping purposes

# based on RFC 1035: https://datatracker.ietf.org/doc/html/rfc1035
# also RFC RFC 3596 for AAAA: https://datatracker.ietf.org/doc/html/rfc3596

from socket import AF_INET, SOCK_DGRAM, socket, connect, send, receive
from ctypes import c_ubyte, c_ushort, c_short
from dataclass import dataclass

# Part A: Globals

QUERY 		= 0				# marks if query
RESPONSE 	= 1				# marks if response
SQUERY 		= 0				# marks standard query
AUTHQUERY	= 1				# marks if authorative response
TRUNC 		= 1				# marks if response is truncated
RECURDESIRE = 1				# marks if recursion is desired
RECURNOTDES = 0				# marks if recursion is not desired
RECURAVAIL  = 1				# marks if recursion is available
RECURNOTAV  = 0				# marks if recursion is not available
ZERO        = 0				# marks the zero preserved field
NOERR		= 0				# marks no error
FROMATERR 	= 1				# marks format error 
SERVERFAIL  = 2				# marks server failure
NAMEERR	    = 3				# marks name error
NOTIMPLMNT  = 4				# marks not implemented error
REFUSED     = 5				# marks refused error
INTERNET    = 1				# marks internet class
ARECORD     = 1				# marks A record type
CNAMERECORD = 5				# marks CNAME record type
TXTRECORD   = 16			# marks TXT record type
AAAARECORD  = 28			# marks AAAA record type

# Part B: Types

# this is the header for both response and question

@dataclass 
class DNSQueryHeader:
	xid = c_ushort(0)		# a random 16-bit unsigned ID
	qr = c_ubyte(0)			# question or response? One bit only
	opcode = c_ubyte(0)		# four bits. What type of query is it? We always set it to squery (standard querey)
	aa = c_ubyte(0)			# Authoratic Answer or not  --- one bit
	tc = c_ubyte(0)			# has it be truncated? one bit
	rd = c_ubyte(0)			# only in question, is recursion desired? --- one bit
	ra = c_ubyte(0)			# only in response, is recursion available? --- one bit
	z = c_ubyte(0)			# always set to 0 --- one bit
	rcode = c_ubyte(0)		# response code, 4 bits
	qdcount = c_ushort(0)   # 16-bit unsigned, question count
	ancount = c_ushort(0)   # 16-bit unsigned, answer count
	nscount = c_ushort(0) 	# 16-bit unsigned, name authority record count
	arcount = c_ushort(0)   # 16-bit unsigned, additional record count

# this is format of a question, there can be several, but we'll just send one

@dataclass
class DNSQueryQuestion:
	qname = [c_ubyte(0)]	# variable, name of the desired domain, null-terminated
	qtype = c_short(0)		# type of the question, 16-bit unsigned
	qclass = c_short(0) 	# class of the question, 16-bit unsigned

# this is format of a response resource record, there can be several, but we'll just send one

@dataclass
class DNSResourceRecord:
	name = [c_ubyte(0)]  	# variable, human-readable name of the domain
	rtype = c_ushort(0)  	# unsigned 16-bit integer, type of the resource
	rclass = c_ushort(0) 	# unsigned 16-bit integer, class of the resource
	ttl = c_ushort(0)    	# unsigned 16-bit integer, time interval until caching is valid
	rdlength = c_ushort(0) 	# unsigned 16-bit integer, length of rdata
	rdata = [c_ubyte(0)]   	# variable, the data, for A and AAA it's the IPV4 and IPV6

