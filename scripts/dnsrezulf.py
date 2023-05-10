# Please see LICENSE for info on distribution

# this file contain a simple, limited implementation of the
# DNS query system in Python as a part of Panah application
# notice that this script is not a complete implementation 
# and has only been written for prototyping Panah DNS resolver
# please only use for educational/prototyping purposes

# based on RFC 1035: https://datatracker.ietf.org/doc/html/rfc1035

from socket import AF_INET, SOCK_DGRAM, socket, connect, send, receive
from ctypes import c_ubyte, c_ushort, c_short
from dataclass import dataclass

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


@dataclass
class DNSQueryQuestion:
	qname = [c_ubyte(0)]	# name of the desired domain, null-terminated
	qtype = c_ubyte(0)		# type of the question
	qclass = c_ubyte(0) 	# class of the question

@dataclass
class DNSResourceRecord:
	name = [c_ubyte(0)]  	# variable, human-readable name of the domain
	rtype = c_ushort(0)  	# unsigned 16-bit integer, type of the resource
	rclass = c_ushort(0) 	# unsigned 16-bit integer, class of the resource
	ttl = c_ushort(0)    	# unsigned 16-bit integer, time interval until caching is valid
	rdlength = c_ushort(0) 	# unsigned 16-bit integer, length of rdata
	rdata = [c_ubyte(0)]   	# the data, for A and AAA it's the IPV4 and IPV6