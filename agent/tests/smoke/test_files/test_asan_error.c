#include <stdio.h>
#include <stdlib.h>

int main() {
    int *arr = malloc(2 * sizeof(int));
    arr[2] = 42;
    free(arr);
    return 0;
}
