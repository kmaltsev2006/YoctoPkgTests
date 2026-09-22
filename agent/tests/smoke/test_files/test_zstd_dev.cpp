#include <zstd.h>
#include <iostream>

int main() {
    unsigned version = ZSTD_versionNumber();
    if (version > 0) {
        return 0;
    }
    return 1;
}
