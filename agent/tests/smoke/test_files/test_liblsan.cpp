#include <stdlib.h>
#include <stdio.h>
int main() {
    void *p = malloc(1024);
    p = NULL; // Leak
    printf("Program finished, exiting without free...\n");
    return 0;
}