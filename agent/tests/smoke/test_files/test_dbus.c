#include <dbus-1.0/dbus/dbus.h>
#include <stdio.h>
int main() {
    DBusError err;
    dbus_error_init(&err);
    
    if (!dbus_error_is_set(&err)) {
        printf("DBus linked successfully!\n");
    }
    return 0;
}