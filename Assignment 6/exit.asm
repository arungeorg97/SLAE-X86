global _start


section .text

_start:
	push 0x1
	pop eax
	pop ebx			;push pop instead of inc and xor

	int 0x80
