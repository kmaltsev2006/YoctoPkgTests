#include <libdevmapper.h>
#include <stdio.h>

int main() {
    char version[20];
    if (dm_get_library_version(version, sizeof(version))) {
        printf("DEVMAPPER_VERSION_OK: %s\n", version);
        return 0;
    }
    return 1;
}
