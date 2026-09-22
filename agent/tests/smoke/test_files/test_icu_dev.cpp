#include <unicode/utypes.h>
#include <unicode/ucnv.h>
#include <unicode/ustring.h>
#include <stdio.h>

int main() {
    UErrorCode status = U_ZERO_ERROR;
    UConverter *conv = ucnv_open("UTF-8", &status);
    
    if (U_SUCCESS(status) && conv != NULL) {
        printf("ICU_DEV_SUCCESS\\n");
        ucnv_close(conv);
        return 0;
    } else {
        return 1;
    }
}