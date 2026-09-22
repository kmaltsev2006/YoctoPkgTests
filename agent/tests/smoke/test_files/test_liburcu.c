#include <stdio.h>
#include <urcu.h>

int main() {
    rcu_register_thread();

    printf("RCU thread registered\n");

    rcu_unregister_thread();

    return 0;
}
