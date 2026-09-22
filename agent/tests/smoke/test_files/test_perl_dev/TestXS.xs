#include "EXTERN.h"
#include "perl.h"
#include "XSUB.h"

MODULE = TestXS  PACKAGE = TestXS

int
hello_world()
    CODE:
        RETVAL = 42;
    OUTPUT:
        RETVAL