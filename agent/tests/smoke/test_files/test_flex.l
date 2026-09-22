%{
int num_lines = 0;
int num_chars = 0;
%}

%%
\n  { num_lines++; num_chars++; }
.   { num_chars++; }
%%

int main() {
    yylex();
    printf("Number of lines: %d\n", num_lines);
    printf("Number of characters: %d\n", num_chars);
    return 0;
}