#include <sys/acl.h>
#include <stdio.h>
#include <errno.h>

int main() {
    // Test basic ACL functions
    acl_t acl = acl_init(1);  // Initialize ACL
    if (acl == NULL) {
        printf("ACL_INIT_FAILED:%d\\n", errno);
        return 1;
    }
    
    // Test creating ACL entry
    acl_entry_t entry;
    if (acl_create_entry(&acl, &entry) != 0) {
        printf("ACL_CREATE_ENTRY_FAILED:%d\\n", errno);
        acl_free(acl);
        return 1;
    }
    
    // Test setting tag type
    if (acl_set_tag_type(entry, ACL_USER) != 0) {
        printf("ACL_SET_TAG_FAILED:%d\\n", errno);
        acl_free(acl);
        return 1;
    }

    // Test getting set tag type
    acl_tag_t result_tag;
    if(acl_get_tag_type(entry, &result_tag) != 0) {
        printf("ACL_GET_TAG_FAILED:%d\\n", errno);
        acl_free(acl);
        return 1;
    }
    if(result_tag != ACL_USER){
        printf("Unexpected result tag: expected '%d', got '%d'\\n", ACL_USER, result_tag);
        acl_free(acl);
        return 1;
    }

    printf("ACL_FUNCTIONS_WORK\\n");
    acl_free(acl);
    return 0;
}