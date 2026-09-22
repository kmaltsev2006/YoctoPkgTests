#include <stdio.h>
#include <gnutls/gnutls.h>

int main() {
    int ret = gnutls_global_init();
    if (ret < 0) {
        fprintf(stderr, "Init failed: %s\n", gnutls_strerror(ret));
        return 1;
    }
    printf("GnuTLS initialized successfully\n");
    
    gnutls_global_deinit();
    return 0;
}