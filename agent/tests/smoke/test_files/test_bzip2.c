#include <bzlib.h>
#include <stdio.h>
#include <string.h>

int main() {
    char input[] = "Hello bzip2 smoke test";
    char output[100];
    unsigned int outlen = sizeof(output);
    
    int result = BZ2_bzBuffToBuffCompress(
        output, &outlen, input, strlen(input), 1, 0, 0
    );
    
    if (result == BZ_OK) {
        printf("COMPRESSED:%u\\n", outlen);
        return 0;
    } else {
        return 1;
    }
}