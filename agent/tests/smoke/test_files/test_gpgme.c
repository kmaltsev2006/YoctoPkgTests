#include <stdio.h>
#include <gpgme.h>

int main() {
    const char *version = gpgme_check_version(NULL);
    if (!version) {
        fprintf(stderr, "gpgme_check_version failed\n");
        return 1;
    }
    printf("GPGME version: %s\n", version);

    gpgme_ctx_t ctx;
    gpgme_error_t err = gpgme_new(&ctx);
    if (err) {
        fprintf(stderr, "Context creation failed: %s\n", gpgme_strerror(err));
        return 1;
    }
    
    printf("GPGME Context created successfully\n");
    gpgme_release(ctx);
    return 0;
}