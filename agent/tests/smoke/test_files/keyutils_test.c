#include <keyutils.h>
#include <stdio.h>
#include <errno.h>

int main() {
    key_serial_t key;
    
    // Test basic keyctl function
    key = add_key("user", "testkey", "testdata", 8, KEY_SPEC_USER_KEYRING);
    if (key == -1) {
        printf("ADD_KEY_FAILED:%d\\n", errno);
        return 1;
    }
    
    // Test searching for the key
    key_serial_t found_key = keyctl_search(KEY_SPEC_USER_KEYRING, "user", "testkey", 0);
    if (found_key != key) {
        printf("KEYCTL_SEARCH_FAILED\\n");
        return 1;
    }
    
    // Clean up
    keyctl_unlink(key, KEY_SPEC_USER_KEYRING);
    
    printf("KEYUTILS_FUNCTIONS_WORK\\n");
    return 0;
}