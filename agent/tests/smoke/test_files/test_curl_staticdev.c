#include <curl/curl.h>

int main() {
    CURL *c = curl_easy_init();
    return (c == NULL);
}
