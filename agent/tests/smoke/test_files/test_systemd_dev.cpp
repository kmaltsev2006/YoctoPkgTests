#include <systemd/sd-journal.h>
#include <systemd/sd-daemon.h>

int main() {
    sd_journal_print(LOG_INFO, "systemd-dev workability test");
    
    sd_notify(0, "READY=1");
    
    return 0;
}
