#include <stdio.h>
#include <ldap.h>

int main() {
    LDAP *ld;
    int rc;

    rc = ldap_initialize(&ld, "ldap://localhost");
    if (rc != LDAP_SUCCESS) {
        printf("LDAP_INIT_FAIL\n");
        return 1;
    }

    if (ld != NULL) {
        printf("LDAP_OK\n");
    } else {
        printf("LDAP_NULL\n");
        return 1;
    }

    ldap_unbind_ext_s(ld, NULL, NULL);

    return 0;
}
