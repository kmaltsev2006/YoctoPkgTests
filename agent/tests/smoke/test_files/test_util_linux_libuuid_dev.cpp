#include <uuid/uuid.h>
#include <iostream>

int main() {
    uuid_t b_uuid;
    char out[37];

    uuid_generate(b_uuid);
    uuid_unparse(b_uuid, out);

    if (out[0] != '\0') {
        return 0;
    }
    return 1;
}
