#include <avahi-client/client.h>
#include <avahi-common/error.h>
#include <avahi-common/simple-watch.h>
#include <stdio.h>

static void client_callback(AvahiClient *client, AvahiClientState state, void *userdata) {
    printf("CLIENT_STATE_CHANGE:%d\\n", state);
}

int main() {
    AvahiSimplePoll *simple_poll = NULL;
    AvahiClient *client = NULL;
    int error = 0;
    
    // Create simple poll
    simple_poll = avahi_simple_poll_new();
    if (!simple_poll) {
        printf("SIMPLE_POLL_CREATE_FAILED\\n");
        return 1;
    }
    
    // Create client
    client = avahi_client_new(
        avahi_simple_poll_get(simple_poll),
        0,  // flags
        client_callback,
        NULL,  // userdata
        &error
    );
    
    if (!client) {
        printf("CLIENT_CREATE_FAILED:%s\\n", avahi_strerror(error));
        avahi_simple_poll_free(simple_poll);
        return 1;
    }
    
    printf("CLIENT_CREATED_SUCCESSFULLY\\n");
    
    // Cleanup
    avahi_client_free(client);
    avahi_simple_poll_free(simple_poll);
    
    return 0;
}