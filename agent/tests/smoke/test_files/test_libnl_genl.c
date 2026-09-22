#include <stdio.h>
#include <netlink/netlink.h>
#include <netlink/genl/genl.h>
#include <netlink/genl/ctrl.h>

int main() {
    struct nl_sock *sk = nl_socket_alloc();
    if (!sk) return 1;

    int err = genl_connect(sk);
    if (err < 0) {
        nl_socket_free(sk);
        return 2;
    }

    int family_id = genl_ctrl_resolve(sk, "nlctrl");
    if (family_id < 0) {
        nl_socket_free(sk);
        return 3;
    }

    printf("LibNL Genl: Connected and resolved nlctrl family id: %d\n", family_id);
    nl_socket_free(sk);
    return 0;
}