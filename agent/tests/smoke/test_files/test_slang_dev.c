
#include <stdio.h>
#include <slang.h>

int main() {
    // Check if we can access S-Lang version from headers/library
    printf("S-Lang version: %s\n", SLang_Version_String);
    return 0;
}