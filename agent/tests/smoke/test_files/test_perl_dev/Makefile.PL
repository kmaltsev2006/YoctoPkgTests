use ExtUtils::MakeMaker;

WriteMakefile(
    NAME          => 'TestXS',
    VERSION_FROM  => 'TestXS.pm',
    LIBS          => [''],
    DEFINE        => '',
    INC           => '',
    OBJECT        => '$(O_FILES)',
);