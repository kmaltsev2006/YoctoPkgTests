import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('perl-misc tests')
@pytest.mark.smoke
@pytest.mark.perl_misc
class TestPerlMisc:
    '''perl-misc smoke test class'''

    @allure.title('perl-misc: additional modules test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('module', [
        'File::Compare',
        'File::Copy',
        'Getopt::Long',
        'Text::ParseWords',
        'Pod::Usage'
    ])
    def test_perl_misc_modules(self, module: str, ssh_client: SshClient):
        '''Test perl-misc modules installed'''
        with allure.step(f'Checking {module} module'):
            cmd = ssh_client.exec(
                f'perl -M{module} -e "print \\"MODULE_LOADED\\"" 2>&1', ignore_rc=True)
            assert cmd.rc == 0, f"perl-misc failed (module {module} not available): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('perl-misc: module functionality test')
    @pytest.mark.minimal
    def test_perl_misc_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test perl-misc module functionality'''
        with allure.step('Testing File::Copy module'):
            ssh_client.put_file(
                f'{test_files_path}/test_perl_misc/test_copy.pl', remote_tmp_path)
            cmd = ssh_client.exec(
                f'perl {remote_tmp_path}/test_copy.pl', ignore_rc=True)
            assert 'FILE_COPY_MODULE_LOADED' in cmd.stdout, \
                f"perl-misc failed (File::Copy not working): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('perl-misc: Getopt::Long functionality test')
    def test_getopt_long_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test Getopt::Long module functionality'''

        script_file = f'{remote_tmp_path}/test_getopt.pl'
        ssh_client.put_file(
            f'{test_files_path}/test_perl_misc/test_getopt.pl', remote_tmp_path)

        with allure.step('Running Getopt::Long test'):
            cmd = ssh_client.exec(
                f'perl {script_file} --verbose --file=test.txt', ignore_rc=True)
            check.is_in('GETOPT_PARSING_WORKED', cmd.stdout,
                        f"perl-misc failed (Getopt::Long not working): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Verbose: 1', cmd.stdout,
                        f"perl-misc failed (verbose option not parsed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('File: test.txt', cmd.stdout,
                        f"perl-misc failed (file option not parsed): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('perl-misc: Text::ParseWords functionality test')
    def test_text_parsewords_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test Text::ParseWords module functionality'''
        with allure.step('Testing Text::ParseWords'):
            ssh_client.put_file(
                f'{test_files_path}/test_perl_misc/test_parse.pl', remote_tmp_path)
            cmd = ssh_client.exec(
                f'perl {remote_tmp_path}/test_parse.pl', ignore_rc=True)
            assert 'TEXT_PARSEWORKS_WORKS' in cmd.stdout, \
                f"perl-misc failed (Text::ParseWords not working): out='{cmd.stdout}', err='{cmd.stderr}'"
