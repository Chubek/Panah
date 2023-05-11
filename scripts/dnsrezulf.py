# Part of Panah Packet Wrangler: https://github.com/Chubek/Panah
# Released under MIT License, see Panah/LICENSE for more info

# this script contain a simple, limited implementation of the
# DNS query system in Python as a part of Panah application
# notice that this script is not a complete implementation 
# and has only been written for prototyping Panah DNS resolver
# please only use for educational/prototyping purposes

# based on RFC 1035: https://datatracker.ietf.org/doc/html/rfc1035
# also RFC RFC 3596 for AAAA: https://datatracker.ietf.org/doc/html/rfc3596

from socket import AF_INET, SOCK_DGRAM, socket
from dataclasses import dataclass
from time import time_ns

# Part A: Globals & Utils

MAXU16  	= 65535  				    # maximum of u16
ACIIPERIOD  = 46					    # ascii for period

RECURSE_DESIRED 		= 1			    # setting this flag means we want recursive lookup

RCODE_FORMATERROR 		= -1			# these are the 5 return codes of a dns query 
RCODE_SERVREFAIL  		= -2			# format and name error, server fail, implementation issues
RCODE_NAMEERROR 		= -3			# and refused error, you can view all these in RFC 1035 page
RCODE_NOTIMPLEMENTED  	= -4			# 27 --- notice that these are not signed, however, we sign them
RCODE_REFUSED     		= -5			# because we wish to return them as signed values in case of error

ERROR_XIDMATCH			= -6			# these two are the additional errors we wish to add
ERROR_NORECURSION		= -7			# xid mismatch, and no recursion being available in resolver

RCLASS_INTERNET    		= 1				# this is the resource class for internet, we will set it as default for obvious reasosn
QCLASS_ANY				= 255			# this is the 'any' question class, we'll set it as default

RECORD_CNAME 			= 5				# marks CNAME record type
RECORD_A   				= 16			# marks TXT record type
RECORD_AAAA  			= 28			# marks AAAA record type


def generate_random_ushort():
	seed = time_ns()
	return ((seed << 5) + seed) % MAXU16

def error_out(message: str):
	print("\033[1;31mError occured\033[0m")
	print(message)
	exit(1)


def uint_to_inet_str(inet: int) -> str:
	quart_upper_upper = inet & 0xff000000
	quart_upper_lower = inet & 0xff0000
	quart_lower_upper = inet & 0xff00
	quart_lower_lower = inet & 0xff
	return f"{quart_lower_lower}.{quart_lower_upper >> 8}.{quart_upper_lower >> 16}.{quart_upper_upper >> 24}"

# Part B: Types

# this is the header for both response and question

@dataclass 
class DNSQueryHeader:
	xid = 0					# a random 16-bit unsigned ID
	qr = 0					# question or response? One bit only
	opcode = 0				# four bits. What type of query is it? We always set it to squery (standard querey)
	aa = 0					# Authoratic Answer or not  --- one bit
	tc = 0					# has it be truncated? one bit
	rd = 0					# only in question, is recursion desired? --- one bit
	ra = 0					# only in response, is recursion available? --- one bit
	z = 0					# always set to 0 --- three bits
	rcode = 0				# response code, 4 bits
	qdcount = 0   			# 16-bit unsigned, question count
	ancount = 0   			# 16-bit unsigned, answer count
	nscount = 0 			# 16-bit unsigned, name authority record count
	arcount = 0   			# 16-bit unsigned, additional record count

# this is format of a question, there can be several, but we'll just send one

@dataclass
class DNSQueryQuestion:
	qname  = b""			# variable, name of the desired domain, null-terminated
	qtype  = 0				# type of the question, 16-bit unsigned
	qclass = QCLSS_ANY 		# class of the question, 16-bit unsigned

# this is format of a response resource record, there can be several, but we'll just send one

@dataclass
class DNSResourceRecord:
	name      = b""						# variable, human-readable name of the domain
	rtype     = 0  						# unsigned 16-bit integer, type of the resource
	rclass    = RCLASS_INTERNET			# unsigned 16-bit integer, class of the resource
	ttl    	  = 0    					# unsigned 16-bit integer, time interval until caching is valid
	rdlength  = 0 						# unsigned 16-bit integer, length of rdata
	rdata     = b""	   					# variable, the data, for A and AAA it's the IPV4 and IPV6

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
	return DNSQueryQuestion(qname=qname, qtype=qtype)

# make a new header object

def new_dns_query_header(rd=RECURSE_DESIRED):
	return DNSQueryHeader(xid=generate_random_ushort(), rd=rd)

# encode the query header, as specified by the RFC
# the options are 16-bits, and as the net byte order goes, big-endian

def encode_dns_query_header(header: DNSQueryHeader) -> bytearray:
	xid = header.xid.to_bytes(2, byteorder="big")
	options = ((header.qr & 0b1) | ((header.opcode << 15) & 0b1111) | ((header.aa << 11) & 0b1) | ((header.tc << 10) & 0b1) | (header.rd << 9) | ((header.ra << 8) & 0b1) | ((header.z << 7) & 0b1111) | (header.rcode & 0b11111)).to_bytes(2, byteorder='big')
	qdcount = header.qdcount.to_bytes(2, byteorder='big')
	ancount = header.anqount.to_bytes(2, byteorder='big')
	nscount = header.nscount.to_bytes(2, byteorder='big')
	arcount = header.arcount.to_bytes(2, byteorder='big')
	return xid + options + qdcount + ancount + nscount + arcount


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
	options = int.from_bytes(response[2:4], byteorder="big", signed=False)
	qr = (options & 32768) >> 15
	opcode = (options & 32720) >> 11
	aa = (options & 1024) >> 10
	tc = (options & 256) >> 9
	rd = (options & 128) >> 8
	ra = (options & 64) >> 7
	z  = (options & 0b1110000) >> 4
	rcode = (options & 15)
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


def generate_and_compose_query(address: str, rectype=ARECORD, recursive=RECURSE_DESIRED) -> tuple[bytes, int]:
	header = new_dns_query_header(recursive)
	question = new_dns_query_question(address, rectype)
	return encode_dns_query_packet(header, question), header.xid


def parse_server_response(response: bytearray, xid: int, recursion=RECURSE_DESIRED) -> bytes:
	header = decode_dns_query_header(response)
	# check for errors in response
	if header.xid != xid:
		return ERROR_XIDMISMATCH		# the XID given does not match with XID returned
	if header.ra != recursion:
		return ERROR_NORECURSION		# if we have set recursion to true, and server does not support it
	if not header.rcode:
		return -header.rcode          	# we sign-extend the rcode if it is non-zero and return it
	record = decode_dns_query_resource_record(response)
	return record.rdata            		# we return the rdata, other parts are not desired


# Part D: Resolver

# the resolver interface puts everything we made prior together

class DNSResolver:
	def __init__(self, resolver="8.8.8.8", port=53):
		self.resolver = resolver
		self.port = port
		self.socket = socket(AF_INET, SOCK_DGRAM)							# open a socket to the resolver server

	def connect_to_resolver(self):
		self.socket.connect(self.resolver, self.port)						# connect to the socket

	def send_and_receive_query(self, addr: str, rectype=ARECORD, recursion=RECURSE_DESIRED, retries=3) -> bytes:
		packet, xid = generate_and_compose_query(addr, rectype, recursion)  # generate the packet
		lenpaacket = len(packet)
		sent = self.socket.send(packet)										# send the packet
		while sent != lenpacket and retries > 0:							# retry if send fails
			sent = self.socket.send(packet)
		response = []
		while True:
			received_data = self.recv(1024)									# get the response
			if received_data is None:
				break
			response.extend(received_data)
		return parse_server_response(response, xid, recursion)				# parse the response

	def close_connection(self):
		self.socket.shutdown()


# Part E: Command Line Interface

if __name__ == "__main__":
	from sys import argv, executable
	execname = executable.split("/")[-1]
	scriptname = argv[0]

	options = []										# we pre-declare the options list because we wanna reference it to print_help_and_exit
	
	def choose_record_type(_, rectype: str) -> tuple[int, str, callable]:	# this function parses the record type
		if rectype == "A":
			return RECORD_A, "A", uint_to_inet_str
		elif rectype == "AAAA":
			return RECORD_AAAA, "AAAA", int
		elif rectype == "CNAME":
			return RECORD_CNAME, "CNAME", str
		else:
			error_out("Wrong record type, can only be A, AAAA, or CNAME")

	def choose_recursion(rec: bool) -> int:				# this function parses the recursion flag
		if rec:
			return RECURDERSIRE
		else:
			return RECURNOTDES
  														# this function error-checks string options
	def set_string_option(arg: str, option: str) -> str: 
		if arg is None:									# for both this and the next one, we return
			return option 								# the option if the first parameter is None
		if option.isdigit(): 							# so that we can pass defaults to them too
			error_out(f"Numeric argument passed for {arg}")
		return option
														# this function error-checks numeric arguments
	def set_integer_option(arg: str, option: str, range=(0, 65535)) -> int:
		if arg is None:
			return option
		if not option.isdigit():
			error_out(f"Non-numeric argument passed for {arg}")
		parsed = int(option)
		if parsed < range[0] or parsed > range[1]:
			error_out(f"Argument passed for {arg} is not in range ([{range[0]}, {range[1]}])")

	def print_help_and_exit(_, options=options):		# this function is for composing and printing help
		argmsg = "\n".join([f"[{l}/{s}]\t{h}\tDefault: {d}" for l, s in [(f[0], f[1], f[4], f[2]) for f in options]])
		print("\033[1;33mDNS Resolver by Chubak Bidpaa\033[0m")
		print("Usage:")
		print(execname, scriptname, argmsg)
		print("Example:")
		print(execname, scriptname, "--record-type AAAA")
		exit(1)

													# arguments/options in form (long, short, default, parser, help)
	options = [
		("--address", "-ad", "example.com", set_string_option, "The address to resolve"),
		("--resolver", "-rs", "8.8.8.8", set_string_option, "The DNS resolver"),
		("--port", "-p", 53, set_integer_option, "The resolver port"),
		("--record-type", "-rt", "A", choose_record_type, "The query record (A, AAAA or CNAME)"),
		("--recursion", "-rc", True, choose_recursion, "Recursion flag (no argument)"),
		("--retries", "-re", 5, lambda *a, **k: set_integer_options(*a, **k, range=(0, 30)), "Number of retries in case connection fails"),
		("--help", "-h", "N/A", print_help_and_exit, "Show help")

	]
													  # this function parses the arguments, based on the following argument
													  # we must give it one of the flag list members, expanded with asterisk
	def parse_arg_or_default(arg, next_arg, long, short, default, func, _):
		if arg == long or arg == short:
			return func(arg, next_arg)
		else:
			return func(None, default)

													  # same as before, except it does not take the next argument, since it's a flipper
	def parse_flag_or_default(arg, long, short, default, func, _):
		if arg == long or arg == short:
			return func(True)						  # if the flag has been passed, this means it's true
		else:
			return func(default)

	argv.append(None)								  # we must append a dummy to argv, it has be default one member and we need two to set our options

	for arg, next_arg in zip(argv[::2], argv[1::2]):  # we zip even and odd members of argv
		address = parse_arg_or_default(arg, next_arg, *options[0])
		resolver = parse_arg_or_default(arg, next_arg, *options[1])
		port = parse_arg_or_default(arg, next_arg, *options[2])
		rectype, recstr, recfunc = parse_arg_or_default(arg, next_arg, *options[3])
		recursion = parse_flag_or_default(arg, *options[4])
		retries = parse_arg_or_default(arg, next_arg, *options[5])
		_ = parse_arg_or_default(arg, *options[6])
													   # this loop will set the default values either way

	# final showdown

	dnsresolver = DNSResolver(resolver, port)
	dnsresolver.connect_to_resover()
	data = dnsresolver.send_and_receive_query(address, rectype, recursion, retries)
	dnsresolver.close_connection()

	# checking for errors that we set before in case of something going wrong	

	if data < 0:
		if data == ERROR_XIDMISMATCH:
			error_out("XID match error")
		elif data == ERROR_NORECURSION:
			error_out("Resolver has no recursion available")
		elif data == RCODE_FORMATERROR:
			error_out("Format error")
		elif data == RCODE_NAMEERROR:
			error_out("Name error")
		elif data == RCODE_REFUSED:
			error_out("Server refused connection")
		elif data == RCODE_NOTIMPLEMENTED:
			error_out("Server does not have this feature implemented")
		elif data == RCODE_SERVERFAIL:
			error_out("Server responded with a FAIL message")
		else:
			error_out("Server responded with an unknown response code")


	print(f"{recstr}\t|\t{recfunc(data)}")