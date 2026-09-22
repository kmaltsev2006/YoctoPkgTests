#include <stdio.h>
#include <readline/readline.h>
#include <readline/history.h>

int main() {
    // Just initialize and check version string to verify headers/lib linkage
    printf("Readline version: %s\n", rl_library_version);
    return 0;
}
