#include <iostream>
#include <vector>
#include <gsl/span>

int main() {
    std::vector<int> data = {1, 2, 3, 4, 5};
    
    gsl::span<int> my_span = data;
    
    if (my_span.size() == 5 && my_span[0] == 1 && my_span[4] == 5) {
        std::cout << "GSL span initialized successfully" << std::endl;
        return 0;
    }
    
    std::cerr << "GSL span logic failed" << std::endl;
    return 1;
}