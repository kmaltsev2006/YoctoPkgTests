#include <gflags/gflags.h>

DEFINE_bool(tmp, true, "tmp");

int main(int argc, char** argv) {
    gflags::ParseCommandLineFlags(&argc, &argv, true);
    return FLAGS_tmp ? 0 : 1;
}
