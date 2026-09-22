use Getopt::Long;

my $verbose = 0;
my $help = 0;
my $file = '';

# Test Getopt::Long parsing
GetOptions(
    'verbose' => \$verbose,
    'help'    => \$help,
    'file=s'  => \$file,
) or die "Usage: $0 [--verbose] [--help] [--file=filename]\n";

print "GETOPT_PARSING_WORKED\n";
print "Verbose: $verbose\n" if $verbose;
print "Help: $help\n" if $help;
print "File: $file\n" if $file;