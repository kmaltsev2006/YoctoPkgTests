#include <stdio.h>
#include <stdint.h>
#include <lzlib.h>

int main() {
    const char *ver = LZ_version();
    
    if (ver) {
        printf("lzlib version: %s\n", ver);
        return 0;
    }
    
    fprintf(stderr, "Failed to get lzlib version\n");
    return 1;
}