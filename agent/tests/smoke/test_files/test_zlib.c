#include <stdio.h>
#include <string.h>
#include <zlib.h>
int main(){
    const char *s = "hello zlib";
    unsigned char out[100];
    unsigned long outlen = sizeof(out);
    if (compress(out, &outlen, (const unsigned char*)s, strlen(s)+1) != Z_OK) return 1;
    printf("COMPRESSED:%lu\n", outlen);
    return 0;
}