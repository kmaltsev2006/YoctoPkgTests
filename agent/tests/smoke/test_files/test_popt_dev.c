#include <popt.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int opt;
    int flag = 0;
    char *value = NULL;
    
    struct poptOption options[] = {
        {"flag", 'f', POPT_ARG_NONE, &flag, 0, "Set flag", NULL},
        {"value", 'v', POPT_ARG_STRING, &value, 0, "Set value", "STRING"},
        POPT_AUTOHELP
        POPT_TABLEEND
    };
    
    poptContext context = poptGetContext(NULL, argc, (const char **)argv, options, 0);
    
    while ((opt = poptGetNextOpt(context)) >= 0) {
    }
    
    if (opt < -1) {
        fprintf(stderr, "Error: %s\n", poptStrerror(opt));
        poptFreeContext(context);
        return 1;
    }
    printf("POPT_LIBRARY_WORKS\n");
    if (flag) {
        printf("Flag was set\n");
    }
    
    if (value != NULL) {
        printf("Value: %s\n", value);
    }
    
    poptFreeContext(context);
    return 0;
}