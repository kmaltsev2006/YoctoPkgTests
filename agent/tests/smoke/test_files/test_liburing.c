#include <liburing.h>
#include <stdio.h>

int main(void)
{
    struct io_uring ring;
    int ret;

    ret = io_uring_queue_init(1, &ring, 0);
    if (ret < 0) {
        fprintf(stderr, "io_uring_queue_init failed: %d\n", ret);
        return 1;
    }

    io_uring_queue_exit(&ring);
    return 0;
}
