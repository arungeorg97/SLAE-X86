**Assignment 6**

Polymorphic Linux Shellcode 



For this Assignment, we have to create polymorphic shellcode of  3 common shellcodes from shell-storm.org.

	Goal is to change the bits around ,add some junk instructions and trim off unnecassary instruction but keep the original functionality intact.


**Methadology**

	Following Shellcodes are considered for polymorphism

		>chmod /etc/shadow with 0666 permisssion
			Refer : http://shell-storm.org/shellcode/files/shellcode-556.php

		>add an entry in /etc/hosts
			Refer : http://shell-storm.org/shellcode/files/shellcode-893.php

		>sys_exit(0)
			Refer : http://shell-storm.org/shellcode/files/shellcode-623.php


**Github Repo**

This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification: http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert/

Student ID: SLAE-1509
