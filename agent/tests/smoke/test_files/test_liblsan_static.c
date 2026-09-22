#include <stdlib.h>
int main() {
  void **p = malloc(42); // leak (categorized as "Direct leak")
  *p = malloc(43);       // leak (categorized as "Indirect leak")
  p = 0;
}