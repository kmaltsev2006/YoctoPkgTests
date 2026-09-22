#include <zmq.h>
#include <assert.h>

int main() {
    void *context = zmq_ctx_new();
    if (context == nullptr) return 1;
    zmq_ctx_term(context);
    return 0;
}
