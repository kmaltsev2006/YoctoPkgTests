#include <stdio.h>

struct test_struct {
    int a;
    char b;
    long c;
};

int main() {
    struct test_struct s = {1, 'a', 100};
    printf("TEST_STRUCT_CREATED\\n");
    return 0;
}