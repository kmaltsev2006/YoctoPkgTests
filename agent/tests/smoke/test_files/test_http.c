#include <stdio.h>
#include <http_parser.h>

int main() {
    http_parser parser;
    http_parser_init(&parser, HTTP_REQUEST);
    unsigned long version = http_parser_version();
    printf("Parser initialized, version: %lu\n", version);
    return 0;
}