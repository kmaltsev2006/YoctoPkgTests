#include <zstd.h>
#include <stdio.h>

int main() {
    unsigned version = ZSTD_versionNumber();
    if (version > 0) {
        printf("ZSTD_VERSION_OK_%u", version);
        return 0;
    }
    return 1;
}
