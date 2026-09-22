#include <krb5.h>
#include <stdio.h>
#include <string.h>

int main() {
    krb5_context context;
    krb5_error_code ret;
    
    // Test krb5_init_context
    ret = krb5_init_context(&context);
    if (ret != 0) {
        printf("KRB5_INIT_CONTEXT_FAILED:%d\\n", ret);
        return 1;
    }
    
    // Test getting default realm
    char *realm;
    ret = krb5_get_default_realm(context, &realm);
    if (ret == 0 && realm != NULL) {
        printf("Default realm: %s\\n", realm);
        krb5_free_default_realm(context, realm);
    }
    
    // Test error message facility
    const char *error_msg = krb5_get_error_message(context, ret);
    if (error_msg != NULL) {
        printf("Error message facility works\\n");
        krb5_free_error_message(context, error_msg);
    }
    
    krb5_free_context(context);
    printf("KRB5_FUNCTIONS_WORK\\n");
    return 0;
}