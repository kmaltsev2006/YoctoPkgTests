#include <systemtap/stapmark.h>

int main() {
    // Check if the STAP_PROBE macro from systemtap-dev is available
    STAP_PROBE(test_provider, test_probe);
    return 0;
}
