#include <stdatomic.h>
#include <stdio.h>
#include <stdbool.h>

int main() {
    // Test atomic operations
    atomic_int counter = ATOMIC_VAR_INIT(0);
    
    // Test atomic_fetch_add
    int old_value = atomic_fetch_add(&counter, 5);
    if (old_value != 0) {
        printf("ATOMIC_FETCH_ADD_FAILED\\n");
        return 1;
    }
    
    // Test atomic_load
    int current = atomic_load(&counter);
    if (current != 5) {
        printf("ATOMIC_LOAD_FAILED\\n");
        return 1;
    }
    
    // Test atomic_store
    atomic_store(&counter, 10);
    current = atomic_load(&counter);
    if (current != 10) {
        printf("ATOMIC_STORE_FAILED\\n");
        return 1;
    }
    
    printf("LIBATOMIC_FUNCTIONS_WORK\\n");
    return 0;
}