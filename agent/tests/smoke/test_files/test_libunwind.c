#include <libunwind.h>
#include <stdio.h>

static void unwind_test(void) {
    unw_cursor_t cursor;
    unw_context_t context;

    unw_getcontext(&context);
    unw_init_local(&cursor, &context);

    int frames = 0;
    while (unw_step(&cursor) > 0) {
        frames++;
    }

    if (frames > 0) {
        printf("UNWIND_OK\n");
    }
}

int main(void) {
    unwind_test();
    return 0;
}
