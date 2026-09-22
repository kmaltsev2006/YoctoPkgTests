#define _GNU_SOURCE
#include <bsd/string.h>
#include <stdio.h>
#include <string.h>

int main() {
    char dest[20] = {0};
    const char *src = "Hello, World!";
    
    // Test strlcpy from libbsd
    size_t result = strlcpy(dest, src, sizeof(dest));
    
    if (result != strlen(src)) {
        printf("STRLCPY_FAILED: expected %zu, got %zu\\n", strlen(src), result);
        return 1;
    }
    
    if (strcmp(dest, src) != 0) {
        printf("STRLCPY_CONTENT_FAILED\\n");
        return 1;
    }
    
    // Test strlcat
    char dest2[30] = "Prefix: ";
    result = strlcat(dest2, src, sizeof(dest2));
    
    if (strcmp(dest2, "Prefix: Hello, World!") != 0) {
        printf("STRLCAT_FAILED\\n");
        return 1;
    }
    
    printf("LIBBSD_FUNCTIONS_WORK\\n");
    return 0;
}