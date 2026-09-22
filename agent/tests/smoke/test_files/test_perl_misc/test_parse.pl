use Text::ParseWords;

my $text = 'word1,word2,"quoted word",word3';
my @words = parse_line(',', 0, $text);

print "PARSED_WORDS: " . scalar(@words) . "\n";
for my $i (0..$#words) {
    print "Word $i: $words[$i]\n";
}

if (scalar(@words) == 4) {
    print "TEXT_PARSEWORKS_WORKS\n";
}