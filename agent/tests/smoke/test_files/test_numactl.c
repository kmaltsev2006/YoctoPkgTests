#include <stdio.h>
#include <numa.h>

int main() {
    if (numa_available() != -1) {
        printf("NUMA_OK\n");
        return 0;
    } else {
        return 1;
    }
}
