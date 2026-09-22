#include <stdio.h>
#include <netlink/netlink.h>
#include <netlink/socket.h>
#include <netlink/route/link.h>

int main() {
    struct nl_sock *sk = nl_socket_alloc();
    if (!sk) return 1;
    
    // Just minimal checks for linkage
    printf("LibNL Core: Socket created.\n");
    nl_socket_free(sk);
    return 0;
}