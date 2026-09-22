#include <stdio.h>
#include <pcap.h>

int main() {
    pcap_t *handle;
    handle = pcap_open_dead(1, 65535); // 1 = Ethernet
    
    if (handle == NULL) {
        fprintf(stderr, "Error: pcap_open_dead returned NULL\n");
        return 1;
    }
    printf("libpcap initialized successfully. Handle created.\n");

    int linktype = pcap_datalink(handle);
    if (linktype == 1) {
        printf("Linktype verified: Ethernet\n");
    } else {
        printf("Linktype mismatch: got %d\n", linktype);
    }
    pcap_close(handle);
    return 0;
}