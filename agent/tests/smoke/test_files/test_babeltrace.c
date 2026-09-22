#include <babeltrace/babeltrace.h>
#include <stdio.h>

int main() {
    struct bt_context *ctx;

    ctx = bt_context_create();
    if (!ctx) {
        printf("FAILED: bt_context_create\\n");
        return 1;
    }
    printf("CONTEXT_CREATED\\n");

    bt_context_get(ctx);
    printf("CONTEXT_GET\\n");

    bt_context_put(ctx);
    bt_context_put(ctx);
    printf("CONTEXT_PUT\\n");

    printf("SUCCESS\\n");
    return 0;
}