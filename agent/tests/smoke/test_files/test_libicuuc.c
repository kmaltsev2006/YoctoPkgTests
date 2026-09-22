#include <stdio.h>
#include <unicode/utypes.h>
#include <unicode/putil.h>
#include <unicode/uclean.h>

int main() {
    UVersionInfo versionArray;
    char versionString[16];
    UErrorCode status = U_ZERO_ERROR;

    u_init(&status);
    if (U_FAILURE(status)) {
        printf("ICU Initialization failed\n");
        return 1;
    }

    u_getVersion(versionArray);
    u_versionToString(versionArray, versionString);

    printf("ICU Version: %s\n", versionString);
    return 0;
}