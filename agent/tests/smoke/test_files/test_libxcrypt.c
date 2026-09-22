#include <stdio.h>
#include <unistd.h>
#include <crypt.h>
#include <string.h>

int main() {
    const char *passwd = "password";
    const char *salt = "ab";
    char *hashed = crypt(passwd, salt);

    if (hashed && strcmp(hashed, "") != 0) {
        printf("CRYPT_OK\n");
        return 0;
    } else {
        return 1;
    }
}
