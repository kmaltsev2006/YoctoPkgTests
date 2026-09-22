#include <stdio.h>
#include <stdlib.h>

int main() {
    // Simple test that can be compiled with ASAN
    int *array = malloc(10 * sizeof(int));
    
    if (array == NULL) {
        printf("MALLOC_FAILED\\n");
        return 1;
    }
    
    // Access array (should be fine)
    for (int i = 0; i < 10; i++) {
        array[i] = i;
    }
    
    // Intentionally cause buffer overflow (ASAN should catch this)
    // Note: We don't actually want to cause a crash in the test
    // Just verify we can compile with ASAN flags
    
    free(array);
    printf("ASAN_COMPILATION_WORKS\\n");
    return 0;
}