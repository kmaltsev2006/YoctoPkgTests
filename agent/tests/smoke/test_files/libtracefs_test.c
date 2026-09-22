#include <stdio.h>
#include <tracefs.h>

int main() {
    const char *trace_dir = tracefs_tracing_dir();
    if (trace_dir == NULL) {
        printf("TRACEFS_NOT_FOUND\\n");
    } else {
        printf("TRACEFS_FOUND\\n");
    }
    printf("LIBTRACEFS_TEST_PASS\\n");
    return 0;
}