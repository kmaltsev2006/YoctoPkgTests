#include <iostream>
#include <snappy.h>
#include <string>

int main() {
    std::string input = "snappy_test_data_2026";
    std::string compressed;
    snappy::Compress(input.data(), input.size(), &compressed);
    
    if (!compressed.empty()) {
        std::cout << "Snappy compression works" << std::endl;
        return 0;
    }
    return 1;
}
