#include <libxml/parser.h>
#include <libxml/tree.h>
#include <stdio.h>

int main() {
    char *content = "<root>LIBXML2_WORKS</root>";
    xmlDocPtr doc = xmlReadMemory(content, strlen(content), "noname.xml", NULL, 0);
    if (doc == NULL) return 1;
    
    xmlNodePtr root = xmlDocGetRootElement(doc);
    printf("%s", root->content == NULL ? "PARSED" : "ERROR");
    
    xmlFreeDoc(doc);
    xmlCleanupParser();
    return 0;
}
