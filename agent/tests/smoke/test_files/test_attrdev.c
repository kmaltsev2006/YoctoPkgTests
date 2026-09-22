#include <attr/attributes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    // Test basic attribute operations using libattr
    const char* path = "/tmp/libattr_test_file";
    const char* name = "user.libattr_test";
    char* value = "test_value_libattr";
    char get_value[100];
    int size = 100;
    
    // Create a test file
    FILE* f = fopen(path, "w");
    if (!f) {
        printf("FILE_CREATE_FAILED\\n");
        return 1;
    }
    fclose(f);
    
    // Set attribute using libattr
    int set_result = attr_set(path, name, value, strlen(value), 0);
    if (set_result != 0) {
        printf("ATTR_SET_FAILED:%d\\n", set_result);
        remove(path);
        return 1;
    }
    
    // Get attribute using libattr
    int get_result = attr_get(path, name, get_value, &size, 0);
    if (get_result != 0) {
        printf("ATTR_GET_FAILED:%d\\n", get_result);
        remove(path);
        return 1;
    }
    
    // Check the value
    if (strcmp(get_value, value) != 0) {
        printf("VALUE_MISMATCH:%s\\n", get_value);
        remove(path);
        return 1;
    }
    
    printf("LIBATTR_WORKS:%s\\n", get_value);
    remove(path);
    return 0;
}