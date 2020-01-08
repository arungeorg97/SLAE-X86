**Assignment 5**

	Analyze 3 msfvenom payloads and see whats going on under the hood.

**Introduction**

	Payloads provdided by msfvenom for  linux_x86 environment can be listed using the command
			msfvenom  --list payloads |grep linux/x86/ 


	I have choosen the following payloads for this assignment

			>linux/x86/adduser 
			>linux/x86/exec
			>linux/x86/shell_bind_tcp


**Tools used**

		GDB debugger with Peda extention
		
		Refer:
			https://www.gnu.org/software/gdb/
			https://github.com/longld/peda


**Github Repository**

This blog post has been created for completing the requirements of the SecurityTube Linux Assembly Expert certification: http://securitytube-training.com/online-courses/securitytube-linux-assembly-expert/

Student ID: SLAE-1509
