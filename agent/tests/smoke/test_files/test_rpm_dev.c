#include <rpm/rpmlib.h>
#include <stdio.h>

int main() {
    // Check if we can access RPM macros/versions from headers
    printf("RPM version from header: %s\n", RPMVERSION);
    return 0;
}
