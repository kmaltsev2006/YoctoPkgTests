#include <nettle/sha2.h>
#include <string.h>

int main() {
    struct sha256_ctx ctx;
    uint8_t digest[SHA256_DIGEST_SIZE];
    const char* msg = "simple";

    sha256_init(&ctx);
    sha256_update(&ctx, strlen(msg), (const uint8_t*)msg);
    sha256_digest(&ctx, SHA256_DIGEST_SIZE, digest);

    return 0;
}