#include <cups/cups.h>

int main() {
    cups_dest_t *dests;
    int num_dests = cupsGetDests(&dests);
    return 0;
}
