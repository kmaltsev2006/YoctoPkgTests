#include <stdio.h>
#include <openssl/sha.h>
#include <string.h>

int main() {
    const char *msg = "hello";
    unsigned char hash[SHA256_DIGEST_LENGTH];

    if (!SHA256((const unsigned char*)msg, strlen(msg), hash)) {
        fprintf(stderr, "SHA256 failed\n");
        return 1;
    }
    
    printf("OPENSSL_OK\n");
    return 0;
}
