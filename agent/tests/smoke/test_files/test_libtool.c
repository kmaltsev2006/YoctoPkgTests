#include "test_lib.h"
#include <stdio.h>

int main() {
    int sum = add_numbers(5, 3);
    int product = multiply_numbers(5, 3);
    
    if (sum == 8 && product == 15) {
        printf("LIBTOOL_TEST_PASSED\\n");
        return 0;
    } else {
        printf("LIBTOOL_TEST_FAILED: sum=%d, product=%d\\n", sum, product);
        return 1;
    }
}