#include <iostream>
#include <gperftools/tcmalloc.h>

int main() {
    void* ptr = tc_malloc(128);
    
    if (ptr != nullptr) {
        std::cout << "tcmalloc allocation successful" << std::endl;
        tc_free(ptr);
    } else {
        std::cerr << "tcmalloc failed" << std::endl;
        return 1;
    }
    
    return 0;
}