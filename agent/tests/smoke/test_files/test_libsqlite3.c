#include <stdio.h>
#include <sqlite3.h>

int main() {
    sqlite3 *db;
    int rc = sqlite3_open(":memory:", &db);
    if (rc) {
        fprintf(stderr, "Can t open database: %s\n", sqlite3_errmsg(db));
        return 1;
    }
    printf("SQLite3 opened successfully. Lib Version: %s\n", sqlite3_libversion());
    sqlite3_close(db);
    return 0;
}