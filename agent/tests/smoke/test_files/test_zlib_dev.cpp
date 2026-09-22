#include <zlib.h>
#include <iostream>

int main() {
    // Basic check for zlib version and initialization
    const char* version = zlibVersion();
    if (version != nullptr && version[0] != '\0') {
        return 0;
    }
    return 1;
}
