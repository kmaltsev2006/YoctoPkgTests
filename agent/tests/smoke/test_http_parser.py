import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('http-parser tests')
@pytest.mark.smoke
@pytest.mark.http_parser_dev
class TestHttpParserDev:
    '''Tests for the http-parser development library'''

    @allure.title('http-parser-dev: minimal test')
    @pytest.mark.minimal
    def test_http_parser_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of http-parser (headers check)'''
        with allure.step('Check headers'):
            cmd = ssh_client.exec(
                'test -f /usr/include/http_parser.h', ignore_rc=True)
            assert cmd.rc == 0, f"HTTP Parser failed (Header file 'http_parser.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('http-parser-dev: compile and run simple C program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_http_parser_compile(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that http_parser.h exists and libhttp_parser can be linked.
        Compiles a minimal C program using http_parser_init.
        '''
        source_path = f'{remote_tmp_path}/test_http.c'
        binary_path = f'{remote_tmp_path}/test_http_app'

        ssh_client.put_file(
            f'{test_files_path}/test_http.c', remote_tmp_path)

        with allure.step('Compile with -lhttp_parser'):
            cmd = ssh_client.exec(
                f'gcc -o {binary_path} {source_path} -lhttp_parser', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"HTTP Parser failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"HTTP Parser failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('Parser initialized', cmd.stdout,
                        f"HTTP Parser failed (Parser was not initialized): out='{cmd.stdout}', err='{cmd.stderr}'")
