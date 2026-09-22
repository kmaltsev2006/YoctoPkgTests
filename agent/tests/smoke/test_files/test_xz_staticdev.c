#include <lzma.h>
#include <stdio.h>

int main() {
    const char* version = lzma_version_string();
    printf("liblzma version: %s\n", version);
    
    lzma_stream strm = LZMA_STREAM_INIT;
    lzma_ret ret = lzma_easy_encoder(&strm, 6, LZMA_CHECK_CRC64);
    
    if (ret == LZMA_OK) {
        printf("LZMA encoder initialized successfully\n");
        lzma_end(&strm);
        return 0;
    } else {
        fprintf(stderr, "Failed to initialize LZMA encoder: %d\n", ret);
        return 1;
    }
}