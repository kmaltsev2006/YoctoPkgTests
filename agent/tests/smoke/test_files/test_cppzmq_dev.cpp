#include <zmq.hpp>
#include <iostream>

int main() {
    try {
        zmq::context_t ctx(1);
        zmq::socket_t socket(ctx, zmq::socket_type::req);
    } catch (const std::exception &e) {
        std::cerr << e.what();
        return 1;
    }
    return 0;
}
