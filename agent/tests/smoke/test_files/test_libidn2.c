#include <stdio.h>
#include <stdlib.h>
#include <idn2.h>

int main() {
    const char *input = "münchen.de";
    char *output = NULL;
    int rc = idn2_to_ascii_8z(input, &output, 0);

    if (rc != IDN2_OK) {
        fprintf(stderr, "IDN2 error: %s\n", idn2_strerror(rc));
        return 1;
    }

    printf("Punycode: %s\n", output);
    idn2_free(output);
    return 0;
}