global _start


section .text

_start:

	xor eax,eax
	push eax

	push 0x6769666e
	push 0x6f636669
	mov esi,esp

	push eax

	push word 0x632d
	mov edi,esp

	push eax


	push 0x68736162
        push 0x2f6e6962
	push 0x2f2f2f2f

        mov ebx,esp
        push eax


	push esi
	push edi
	push ebx
	mov ecx,esp
	push eax


	xor edx,edx

	mov al,0xb
	int 0x80

