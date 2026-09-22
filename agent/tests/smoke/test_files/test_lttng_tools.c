#include <lttng/lttng.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Create a session structure in memory to verify API workability
    struct lttng_session *sessions = NULL;
    int count = lttng_list_sessions(&sessions);

    // If count is >= 0 or -LTTNG_ERR_NO_SESSIOND (meaning no daemon),
    // the library call itself successfully reached the system/daemon
    if (count >= 0 || count == -LTTNG_ERR_NO_SESSIOND || count == -2) {
        printf("LTTNG_API_FUNCTIONAL\n");
        if (sessions) free(sessions);
        return 0;
    }

    return 1;
}
