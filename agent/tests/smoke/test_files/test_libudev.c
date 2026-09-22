#include <libudev.h>
#include <stdio.h>

int main(void) {
    struct udev *udev;

    udev = udev_new();
    if (!udev) {
        fprintf(stderr, "FAILED\n");
        return 1;
    }

    printf("UDEV_OK\n");
    udev_unref(udev);
    return 0;
}
