use strict;
use warnings;
use JSON;

my %data = (status => q{active}, id => 123);
my $json_text = encode_json \%data;
print "Encoded: $json_text\n";

my $input_json = q|{"message": "hello perl", "code": 200}|;
my $decoded = decode_json $input_json;

if ($decoded->{message} eq q{hello perl} && $decoded->{code} == 200) {
    print "Decoded successfully\n";
} else {
    print "Decoding failed\n";
    exit 1;
}