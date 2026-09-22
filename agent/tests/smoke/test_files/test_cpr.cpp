#include <cpr/cpr.h>
#include <iostream>

int main() {
    cpr::Response r = cpr::Get(cpr::Url{"http://httpbin.org/get"});
    std::cout << "HTTP_STATUS:" << r.status_code << std::endl;
    std::cout << "CPR_LIB_WORKS" << std::endl;
    return 0;
}