#include <stdio.h>
#include <rpcsvc/ypclnt.h>

int main() {
    char *domain = NULL;
    int res = yp_get_default_domain(&domain);
    printf("NSL function executed. Result: %d\n", res);
    return 0;
}