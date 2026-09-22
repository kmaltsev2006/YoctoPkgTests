#include <stdio.h>
#include <traceevent/event-parse.h>

int main() {
    // Test basic traceevent structures
    struct tep_handle *tep;
    
    // Initialize trace event parser
    tep = tep_alloc();
    if (tep == NULL) {
        printf("TEP_ALLOC_FAILED\\n");
        return 1;
    }
    
    // Clean up
    tep_free(tep);
    
    printf("LIBTRACEEVENT_FUNCTIONS_WORK\\n");
    return 0;
}