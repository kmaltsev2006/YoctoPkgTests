#include <stdio.h>
#include <libtasn1.h>

int main() {
    const char *ver = asn1_check_version(NULL);
    if (ver) {
        printf("libtasn1 initialized successfully. Version: %s\n", ver);
        return 0;
    } else {
        fprintf(stderr, "Error: asn1_check_version returned NULL (version mismatch?)\n");
        return 1;
    }
}