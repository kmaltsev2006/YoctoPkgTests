#include <stdio.h>
#include <stdlib.h>
#include <dwarves/dwarves.h>

int main() {
    int result = 0;
    struct cus *cus = cus__new();
    if (cus != NULL) {
        printf("CUS_INIT_SUCCESS\\n");
        cus__delete(cus);
    } else {
        printf("CUS_INIT_NULL\\n");
        result = 1;
    }
    return result;
}