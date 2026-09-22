#include <archive.h>
#include <archive_entry.h>
#include <stdio.h>
#include <string.h>

int main() {
    struct archive *a;
    struct archive_entry *entry;
    
    // Test archive_write_new
    a = archive_write_new();
    if (a == NULL) {
        printf("ARCHIVE_WRITE_NEW_FAILED\\n");
        return 1;
    }
    
    // Test setting format
    if (archive_write_set_format_ustar(a) != ARCHIVE_OK) {
        printf("ARCHIVE_SET_FORMAT_FAILED:%s\\n", archive_error_string(a));
        archive_write_free(a);
        return 1;
    }
    
    // Test archive_entry_new
    entry = archive_entry_new();
    if (entry == NULL) {
        printf("ARCHIVE_ENTRY_NEW_FAILED\\n");
        archive_write_free(a);
        return 1;
    }
    
    archive_entry_set_pathname(entry, "test.txt");
    archive_entry_set_size(entry, 0);
    archive_entry_set_filetype(entry, AE_IFREG);
    
    archive_entry_free(entry);
    archive_write_free(a);
    
    printf("LIBARCHIVE_FUNCTIONS_WORK\\n");
    return 0;
}