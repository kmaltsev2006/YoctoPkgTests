#include <gdbm.h>
#include <stdio.h>
#include <string.h>

int main() {
    GDBM_FILE db = gdbm_open("/tmp/test.db", 0, GDBM_WRCREAT, 0666, 0);
    if (!db) return 1;

    datum key, value, fetched;
    key.dptr = (char*)"mykey"; key.dsize = 5;
    value.dptr = (char*)"myval"; value.dsize = 6;

    if (gdbm_store(db, key, value, GDBM_REPLACE) != 0) return 2;

    fetched = gdbm_fetch(db, key);
    int rc = (fetched.dsize == value.dsize &&
              memcmp(fetched.dptr, value.dptr, value.dsize) == 0) ? 0 : 3;

    gdbm_close(db);
    return rc;
}
