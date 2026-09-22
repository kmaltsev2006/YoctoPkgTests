#include <tirpc/rpc/rpc.h>
#include <stdio.h>
#include <string.h>

int main() {
    // Test basic RPC structures and functions
    struct netconfig *ncp;
    void *handlep;
    if ((handlep = setnetconfig()) == (void *)NULL) {
        printf("SETNETCONFIG_FAILED\\n");
        return 1;
    }
    // Test getnetconfig() - should return network configuration
    ncp = getnetconfig(handlep);
    if (ncp == NULL) {
        printf("GETNETCONFIG_FAILED\\n");
        return 1;
    }
    
    // Test netconfig functions
    const char *proto = ncp->nc_proto;
    if (proto == NULL) {
        printf("NC_PROTO_FAILED\\n");
        return 1;
    }
    
    // Test endnetconfig()
    endnetconfig(ncp);
    
    printf("LIBTIRPC_FUNCTIONS_WORK\\n");
    return 0;
}