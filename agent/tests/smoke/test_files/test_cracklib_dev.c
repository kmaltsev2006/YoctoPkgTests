#include <crack.h>
#include <stdio.h>

int main() {
    const char *passwd = "ComplexPass123!";
    const char *msg = FascistCheck(passwd, NULL);
    return msg ? 1 : 0;
}
