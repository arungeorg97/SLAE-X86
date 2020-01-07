#include<stdio.h>
#include<string.h>

unsigned char code[] = \
"\x6a\x01\x58\x5b\xcd\x80";

int main(void)
{

	printf("shellcode length: %d\n",strlen(code));
	(*(void(*)()) code)();
}
