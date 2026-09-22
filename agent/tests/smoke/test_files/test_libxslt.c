#include <libxslt/xslt.h>
#include <libxslt/transform.h>
#include <libxml/parser.h>

int main() {
    xsltStylesheetPtr cur = NULL;
    xmlDocPtr doc, res;

    xmlSubstituteEntitiesDefault(1);
    xmlLoadExtDtdDefaultValue = 1;

    xsltCleanupGlobals();
    printf("LIBXSLT_INITIALIZED");
    return 0;
}
