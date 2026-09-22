#include <stdio.h>
#include <lmdb.h>

int main() {
    int major, minor, patch;
    char *version = mdb_version(&major, &minor, &patch);
    if (version != NULL) {
        printf("LMDB_VERSION_OK: %s\n", version);
        printf("LMDB_TEST_PASS\n");
        return 0;
    }
    return 1;
}
