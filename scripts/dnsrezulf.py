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
from dataclass import dataclass
from time import time_ns

# Part A: Globals & Utils

QUERY 		= 0				# marks if query
RESPONSE 	= 1				# marks if response
SQUERY 		= 0				# marks standard query
AUTHQUERY	= 1				# marks if authorative response
TRUNC 		= 1				# marks if response is truncated
RECURDESIRE = 1				# marks if recursion is desired
RECURNOTDES				# marks if recursion is not desired
RECURAVAIL  = 1				# marks if recursion is available
RECURNOTAV 				# marks if recursion is not available
ZERO       				# marks the zero preserved field
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
MAXU16  	= 65535  		# maximum of u16
ACIIPERIOD  = 46			# ascii for period

def generate_random_ushort():
	seed = time_ns()
	return ((seed << 5) + seed) % MAXU16

# Part B: Types

# this is the header for both response and question

@dataclass 
class DNSQueryHeader:
	xid					# a random 16-bit unsigned ID
	qr					# question or response? One bit only
	opcode				# four bits. What type of query is it? We always set it to squery (standard querey)
	aa					# Authoratic Answer or not  --- one bit
	tc					# has it be truncated? one bit
	rd					# only in question, is recursion desired? --- one bit
	ra					# only in response, is recursion available? --- one bit
	z					# always set to 0 --- one bit
	rcode				# response code, 4 bits
	qdcount   			# 16-bit unsigned, question count
	ancount   			# 16-bit unsigned, answer count
	nscount 			# 16-bit unsigned, name authority record count
	arcount   			# 16-bit unsigned, additional record count

# this is format of a question, there can be several, but we'll just send one

@dataclass
class DNSQueryQuestion:
	qname				# variable, name of the desired domain, null-terminated
	qtype				# type of the question, 16-bit unsigned
	qclass 				# class of the question, 16-bit unsigned

# this is format of a response resource record, there can be several, but we'll just send one

@dataclass
class DNSResourceRecord:
	name				# variable, human-readable name of the domain
	rtype  				# unsigned 16-bit integer, type of the resource
	rclass 				# unsigned 16-bit integer, class of the resource
	ttl    				# unsigned 16-bit integer, time interval until caching is valid
	rdlength 			# unsigned 16-bit integer, length of rdata
	rdata	   			# variable, the data, for A and AAA it's the IPV4 and IPV6

# Part C: DNS Query Protocol

# qnames in DNS are in form: <len>, <block>, <len>, <block>, ... where each block is separated by period in name

def encode_dns_addr(addr: bytearray) -> bytearray:
	qname = bytearray(0)
	idxcntr = 0
	for i, c in enumerate(addr):
		if c == ASCIIPERIOD:
			qname.append(0)
			idxcntr = i + 1	 	# in case we hit a period, we append a zero which will be the length of the new
			continue			# section and we set the index of counter to it, then we continue
		qname[idxcntr] += 1		# otherwise, we increase the index
		qname.append(c)			# and append the byte
	qname.append(0)				# we must null-terminate
	return qname

# this function is simple, we just set the parameters for header and generate a question

def new_dns_query(addr: str, rectype=ARECORD, recursion=RECURDESIRE) -> tuple[DNSQueryHeader, DNSQueryQuestion]:
	xid = generate_random_ushort()
	qr = QUERY
	opcode = SQUERY
	rd = recursion
	qdcount = 1
	qname = encode_dns_addr(addr)
	qtype = rectype
	qclass = INTERNET
	header = DNSQueryHeader(xid=xid, qr=qr, opcode=opcode, rd=rd, qdcount=qdcount)
	query = DNSQueryQuestion(qname=qname, qtype=qtype, qclass=qclass)
	return header, query

# this function will encode dns query header & question

def encode_query_to_bytes(header: DNSQueryHeader, question: DNSQueryQuestions) -> bytes:
	xid = header.xid.to_bytes(2, byteorder="big")
	flags = ((header.qr & 0b1) | ((header.opcode << 15) & 0b1111) | ((header.aa << 11) & 0b1) | ((header.tc << 10) & 0b1) | (header.rd << 9) | ((header.ra << 8) & 0b1) | ((header.z << 7) & 0b1111) | (header.rcode & 0b11111)).to_bytes(2, byteorder='big')
	qdcount = header.qdcount.to_bytes(2, byteorder='big')
	ancount = header.anqount.to_bytes(2, byteorder='big')
	nscount = header.nscount.to_bytes(2, byteorder='big')
	arcount = header.arcount.to_bytes(2, byteorder='big')
	qname = question.qname
	qtype = question.qtype.to_bytes(2, byteorder='big')
	qclass = question.qclass.to_bytes(2, byteorder='big')
	return xid + flags + qdcount + ancount + nscount + arcount + qname + qtype + qclass

