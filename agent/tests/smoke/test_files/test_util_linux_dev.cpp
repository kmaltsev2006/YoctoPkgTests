#include <libmount/libmount.h>
#include <libsmartcols/libsmartcols.h>
#include <iostream>

int main() {
    // Check libmount
    struct libmnt_context *cxt = mnt_new_context();
    if (!cxt) return 1;
    mnt_free_context(cxt);

    // Check libsmartcols
    struct libscols_table *tb = scols_new_table();
    if (!tb) return 1;
    scols_unref_table(tb);

    return 0;
}
