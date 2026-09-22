#include <gssglue/gssapi/gssapi.h>
#include <stdio.h>
#include <string.h>

int main() {
    OM_uint32 major_status, minor_status;
    gss_buffer_desc name_buffer;
    gss_name_t imported_name;
    
    name_buffer.value = "test@host";
    name_buffer.length = strlen("test@host");
    
    major_status = gss_import_name(&minor_status, &name_buffer, 
                                   GSS_C_NT_HOSTBASED_SERVICE, &imported_name);
    
    if (GSS_ERROR(major_status)) {
        fprintf(stderr, "Failed to import name\n");
        return 1;
    }
    
    printf("libgssglue test successful\n");
    
    gss_release_name(&minor_status, &imported_name);
    
    return 0;
}