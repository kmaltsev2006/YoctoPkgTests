#include <stdio.h>
#include <stdlib.h>
#include <libkmod.h>

int main() {
    struct kmod_ctx *ctx;
    
    ctx = kmod_new(NULL, NULL);
    if (ctx == NULL) {
        fprintf(stderr, "Error: failed to create kmod context\n");
        return 1;
    }

    printf("kmod context initialized successfully\n");
    
    kmod_unref(ctx);
    return 0;
}