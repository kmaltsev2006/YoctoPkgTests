#include <xfs/xfs.h>
#include <xfs/handle.h>
#include <iostream>

int main() {
    void *handp;
    size_t hlen;
    
    path_to_handle((char*)"/", &handp, &hlen);
    
    return 0;
}
