#include <event2/event.h>
#include <stdio.h>

int main() {
    struct event_base *base = event_base_new();
    if (base == NULL) {
        printf("EVENT_BASE_NEW_FAILED\\n");
        return 1;
    }
    printf("LIBEVENT_INITIALIZED\\n");
    event_base_free(base);
    return 0;
}