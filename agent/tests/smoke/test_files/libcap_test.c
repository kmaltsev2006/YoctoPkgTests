#include <sys/capability.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    cap_t caps;
    
    // Test cap_get_proc
    caps = cap_get_proc();
    if (caps == NULL) {
        printf("CAP_GET_PROC_FAILED\\n");
        return 1;
    }
    
    // Test cap_free
    if (cap_free(caps) != 0) {
        printf("CAP_FREE_FAILED\\n");
        return 1;
    }
    
    // Test cap_get_flag (requires initialized caps)
    caps = cap_init();
    if (caps == NULL) {
        printf("CAP_INIT_FAILED\\n");
        return 1;
    }
    
    cap_flag_value_t value;
    if (cap_get_flag(caps, CAP_CHOWN, CAP_EFFECTIVE, &value) != 0) {
        printf("CAP_GET_FLAG_FAILED\\n");
        cap_free(caps);
        return 1;
    }
    
    cap_free(caps);
    
    printf("LIBCAP_FUNCTIONS_WORK\\n");
    return 0;
}