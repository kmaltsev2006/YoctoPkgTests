#include <jansson.h>
#include <stdio.h>

int main() {
    json_t *obj = json_object();
    json_object_set_new(obj, "test", json_string("smoke_test"));
    json_object_set_new(obj, "number", json_integer(42));
    char *json_str = json_dumps(obj, 0);
    printf("JSON:%s\\n", json_str);
    free(json_str);
    json_decref(obj);
    return 0;
}