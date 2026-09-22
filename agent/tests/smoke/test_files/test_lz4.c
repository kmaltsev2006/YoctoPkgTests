#include <stdio.h>
#include <lz4.h>

int main() {
    int version = LZ4_versionNumber();
    printf("LZ4 Version: %d\n", version);
    return 0;
}