#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <linux/perf_event.h>

int main() {
    int result = 0;
    struct perf_event_attr attr;
    memset(&attr, 0, sizeof(attr));
    
    /* Set some basic attributes if constants are defined */
    #ifdef PERF_TYPE_HARDWARE
    attr.type = PERF_TYPE_HARDWARE;
    #endif
    
    #ifdef PERF_COUNT_HW_CPU_CYCLES
    attr.config = PERF_COUNT_HW_CPU_CYCLES;
    #endif
    
    attr.size = sizeof(attr);
    
    printf("PERF_EVENT_STRUCT_SIZE: %zu\\n", sizeof(attr));
    printf("PERF_HEADERS_AVAILABLE\\n");
    
    return result;
}