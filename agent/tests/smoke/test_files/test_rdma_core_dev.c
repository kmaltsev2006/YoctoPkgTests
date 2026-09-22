#include <stdio.h>
#include <infiniband/verbs.h>

int main() {
    int num_devices;
    struct ibv_device **dev_list = ibv_get_device_list(&num_devices);
    
    printf("RDMA devices found: %d\n", num_devices);
    
    if (dev_list) {
        ibv_free_device_list(dev_list);
    }
    
    return 0;
}
