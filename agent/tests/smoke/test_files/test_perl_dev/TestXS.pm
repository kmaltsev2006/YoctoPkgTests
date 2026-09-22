package TestXS;

require Exporter;
require DynaLoader;

our @ISA = qw(Exporter DynaLoader);
our @EXPORT = qw(hello_world);

bootstrap TestXS;

1;