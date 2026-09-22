#include <Python.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    Py_Initialize();
    printf("Python Embedded Success. Version: %s\n", Py_GetVersion());
    Py_Finalize();
    return 0;
}