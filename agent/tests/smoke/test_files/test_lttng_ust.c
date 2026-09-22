#include <lttng/ust-version.h>
#include <stdio.h>

int main() {
    // Check if UST version macros are available from headers
    #if defined(LTTNG_UST_MAJOR_VERSION)
        printf("LTTNG_UST_VERSION_OK: %d.%d\n", LTTNG_UST_MAJOR_VERSION, LTTNG_UST_MINOR_VERSION);
        return 0;
    #else
        return 1;
    #endif
}
