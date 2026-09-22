#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    json j;
    j["name"] = "Alice";
    j["age"] = 25;
    j["list"] = {1, 2, 3};

    std::string s = j.dump();

    json parsed = json::parse(s);
    
    std::string name = parsed["name"];
    int age = parsed["age"];

    return 0;
}
