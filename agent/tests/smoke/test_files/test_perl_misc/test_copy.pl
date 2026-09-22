use File::Copy;

# Test that we can use the module
print "FILE_COPY_MODULE_LOADED\n";

# Test a simple function
my $source = "/etc/passwd";
my $destination = "/tmp/test_copy_$$";

if (-f $source) {
    if (copy($source, $destination)) {
        print "FILE_COPY_SUCCESS\n";
        unlink $destination;
    } else {
        print "FILE_COPY_FAILED: $!\n";
    }
} else {
    print "SOURCE_FILE_NOT_FOUND\n";
}