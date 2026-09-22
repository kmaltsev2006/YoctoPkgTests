#include <stdio.h>
#include <lzma.h>
int main() {
    const char *ver = lzma_version_string();
    if (ver) {
        printf("LZMA Library Version: %s\n", ver);
        return 0;
    }
    return 1;
}