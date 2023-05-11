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
ERRNOXID 	= -1			# error for non-matching XID
ERRNOREC	= -2 			# error for no recursion available
ERRSERVER   = -3   			# error for server fail
ERRANSER 	= -4			# error for answer

def generate_random_ushort():
	seed = time_ns()
	return ((seed << 5) + seed) % MAXU16

def error_out(message: str):
	print("\033[1;31mError occured\033[0m")
	print(message)
	exit(1)

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
	z					# always set to 0 --- three bits
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

# this function will encode the dns address to (len, section, len, section..., NULL) form as specified by the RFC
# basically every section is separated by period (46 ascii) and they must come separated with their length before them
# we then must null-terminate the bytestring

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

# simple, make a new question object

def new_dns_query_question(addr: str, qtype=ARECORD) -> bytearray:
	qname = encode_dns_addr(addr)
	qclass = INTERNET
	return DNSQueryQuestion(qname=qname, qtype=qtype, qclass=qclass)

# make a new header object

def new_dns_query_header(rd=RECURDESIRE):
	return DNSQueryHeader(xid=generate_random_ushort(), rd=rd)

# encode the query header, as specified by the RFC
# the flags are 16-bits, and as the net byte order goes, big-endian

def encode_dns_query_header(header: DNSQueryHeader) -> bytearray:
	xid = header.xid.to_bytes(2, byteorder="big")
	flags = ((header.qr & 0b1) | ((header.opcode << 15) & 0b1111) | ((header.aa << 11) & 0b1) | ((header.tc << 10) & 0b1) | (header.rd << 9) | ((header.ra << 8) & 0b1) | ((header.z << 7) & 0b1111) | (header.rcode & 0b11111)).to_bytes(2, byteorder='big')
	qdcount = header.qdcount.to_bytes(2, byteorder='big')
	ancount = header.anqount.to_bytes(2, byteorder='big')
	nscount = header.nscount.to_bytes(2, byteorder='big')
	arcount = header.arcount.to_bytes(2, byteorder='big')
	return xid + flags + qdcount + ancount + nscount + arcount


def encode_dns_query_question(question: DNSQueryQuestion):
	qtype = question.qtype.to_bytes(2, byteorder="big")
	qclass = question.qclass.to_bytes(2, byteorder="big")
	return question.qname + qtype + qclass

# encode the final packet for request

def encode_dns_query_packet(header: DNSQueryHeader, question: DNSQueryQuestion) -> bytearray:
	return encode_dns_query_header(header) + encode_dns_query_question(question)

# decoding the header is similiar to encoding the header, we just have to reverse the flag and turn bytes into integers instead

def decode_dns_query_header(response: bytes) -> DNSQueryHeader:
	xid = int.from_bytes(response[:2], byteorder="big", signed=False)
	flags = int.from_bytes(response[2:4], byteorder="big", signed=False)
	qr = (flags & 32768) >> 15
	opcode = (flags & 32720) >> 11
	aa = (flags & 1024) >> 10
	tc = (flags & 256) >> 9
	rd = (flags & 128) >> 8
	ra = (flags & 64) >> 7
	z  = (flags & 0b1110000) >> 4
	rcode = (flags & 15)
	qdcount = int.from_bytes(response[4:6], byteorder="big", signed=False)
	ancount = int.from_bytes(response[6:8], byteorder="big", signed=False)
	nscount = int.from_bytes(response[8:10], byteorder="big", signed=False)
	arcount = int.from_bytes(response[10:12], byteorder="big", signed=False)
	return DNSQueryHeader(xid=xid, qr=qr, opcode=opcode, aa=aa, tc=tc, rd=rd, ra=ra, z=z, rcode=rcode, qdcount=qdcount, ancount=ancount, nscount=nscount, arcount=arcount)


# decoding the dns query record is partly similar to the encoding of address
# we must start at byte 12, and add the bytes to our address name until we hit zero
# we then decode type, class and ttl
# after that, we get the length, and grab from that point on, plus rdlength
# that will give us our data

def decode_dns_query_resource_record(response: bytearray) -> DNSResourceRecord:
	name = bytearray()
	for i, c in enumerate(response[12:]):
		if c == 0:
			break
		name.append(c)

	idx = 12 + i
	rtype = int.from_bytes(response[idx:idx + 2], byteorder="big", signed=False)
	rclass = int.from_bytes(response[idx + 2:idx + 4], byteorder="big", signed=False)
	ttl = int.from_bytes(response[idx + 4:idx + 6], byteorder="big", signed=False)
	rdlength = int.from_bytes(response[idx + 6:idx + 8], byteorder="big", signed=False)
	rdata = response[idx + 8:idx + rdlength]
	
	return DNSResourceRecord(name=name, rtype=rtype, rclass=rclass, ttl=ttl, rdlength=rdlength, rdata=rdata)


def generate_and_compose_query(address: str, rectype=ARECORD, recursive=RECURDESIRE) -> tuple[bytes, int]:
	header = new_dns_query_header(recursive)
	question = new_dns_query_question(address, rectype)
	return encode_dns_query_packet(header, question), header.xid


def parse_server_response(response: bytearray, xid: int) -> bytes:
	header = decode_dns_query_header(response)
	if header.xid != xid:
		error_out("XIDs did not match")
	if header.rcode != NOERR:
		if header.rcode == SERVERFAIL:
			error_out("Server failure")
		elif header.rcode == NAMEERR:
			error_out("Name error")
		elif header.rcode == FORMATERROR:
			error_out("Format error")
		else:
			print(f"Undesired rcode: {header.rcode}")
	record = decode_dns_query_resource_record(response)
	return record.rdata


# Part D: Resolver

class DNSResolver:
	def __init__(self, resolver="8.8.8.8", port=53):
		self.resolver = resolver
		self.port = port
		self.socket = socket(AF_INET, SOCK_DGRAM)

	def connect_to_resolver(self):
		self.socket.connect(self.resolver, self.port)

	def send_and_receive_query(self, addr: str, rectype=ARECORD, recursion=RERURDESIRE, retries=3) -> bytes:
		packet, xid = generate_and_compose_query(addr, rectype, recursion)
		lenpaacket = len(packet)
		sent = self.socket.send(packet)
		while sent != lenpacket and retries > 0:
			sent = self.socket.send(packet)
		response = []
		while True:
			received_data = self.recv(1024)
			if received_data is None:
				break
			response.extend(received_data)

		return parse_server_response(response)