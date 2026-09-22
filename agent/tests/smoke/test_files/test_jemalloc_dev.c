#include <stdio.h>
#include <jemalloc/jemalloc.h>
int main() { 
    void *p = malloc(100); 
    free(p); 
    printf("jemalloc test\\n"); 
    return 0; 
}