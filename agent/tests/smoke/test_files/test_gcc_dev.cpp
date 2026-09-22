#include <stdio.h>
#include <stdlib.h>

int main() {
    const char *filename = "/tmp/test_gcc_file.txt";
    FILE *f = fopen(filename, "w");
    if (!f) return 1;
    fprintf(f, "Test output\n");
    fclose(f);

    char buf[100];
    sprintf(buf, "Number: %d", 42);
    printf("%s\n", buf);

    return 0;
}
