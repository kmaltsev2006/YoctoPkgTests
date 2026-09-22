#include <di/di.h>
#include <stdio.h>

int main() {
    const char* version = di_get_version();
    printf("DI library version: %s\n", version);
    return 0;
}