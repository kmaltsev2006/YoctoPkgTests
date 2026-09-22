#include <gflags/gflags.h>
#include <iostream>

DEFINE_bool(testflag, true, "test flag");

int main(int argc, char** argv) {
    gflags::ParseCommandLineFlags(&argc, &argv, true);
    return FLAGS_testflag ? 0 : 1;
}
