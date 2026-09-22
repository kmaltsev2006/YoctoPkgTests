#include <stdio.h>
#include <sodium.h>

int main() {
    if (sodium_init() < 0) {
        fprintf(stderr, "libsodium initialization failed\n");
        return 1;
    }
    printf("Libsodium initialized. Version: %s\n", sodium_version_string());
    return 0;
}