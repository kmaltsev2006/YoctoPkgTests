#include <iostream>
#include <string>
#include <tsl/htrie_map.h>

int main() {
    tsl::htrie_map<char, int> map = {
        {"apple", 1}, {"mango", 2}, {"apricot", 3},
        {"mandarin", 4}, {"melon", 5}, {"macadamia", 6}
    };
    
    auto prefix_range = map.equal_prefix_range("ma");
    int prefix_count = 0;
    for(auto it = prefix_range.first; it != prefix_range.second; ++it) {
        prefix_count++;
    }
    
    if (prefix_count != 3) {
        std::cerr << "Error: should find 3 elements with prefix 'ma', found " << prefix_count << std::endl;
        return 1;
    }
    
    auto longest_prefix = map.longest_prefix("apple juice");
    if(longest_prefix == map.end() || longest_prefix.key() != "apple") {
        std::cerr << "Error: longest prefix of 'apple juice' should be 'apple'" << std::endl;
        return 1;
    }
    
    map.erase_prefix("ma");
    if (map.size() != 3) {
        std::cerr << "Error: after erasing prefix 'ma', map size should be 3, but is " << map.size() << std::endl;
        return 1;
    }
    
    std::cout << "Prefix search test passed" << std::endl;
    return 0;
}