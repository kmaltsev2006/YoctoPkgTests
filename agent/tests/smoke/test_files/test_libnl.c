#include <stdio.h>
#include <netlink/netlink.h>
#include <netlink/socket.h>
#include <netlink/route/link.h>

int main() {
    struct nl_sock *sk = nl_socket_alloc();
    if (!sk) return 1;

    int err = nl_connect(sk, NETLINK_ROUTE);
    if (err < 0) {
        nl_socket_free(sk);
        return 2;
    }

    struct nl_cache *cache;
    err = rtnl_link_alloc_cache(sk, AF_UNSPEC, &cache);
    if (err < 0) {
        nl_socket_free(sk);
        return 3;
    }

    printf("LibNL Core: Socket created, connected, and cache allocated.\n");
    nl_cache_free(cache);
    nl_socket_free(sk);
    return 0;
}