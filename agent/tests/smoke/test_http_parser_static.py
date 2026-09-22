import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('http-parser-staticdev tests')
@pytest.mark.smoke
@pytest.mark.http_parser_dev_static
class TestHttpParserStaticDev:
    '''Tests for the http-parser-static development library'''

    @allure.title('http-parser-staticdev: headers test')
    @pytest.mark.minimal
    def test_http_parser_static_headers(self, ssh_client: SshClient):
        '''Test headers installed'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/http_parser.h', ignore_rc=True)
            assert cmd.rc == 0, f"HTTP Parser Static failed (Header file 'http_parser.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('http-parser-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libhttp_parser.a'
                             ])
    def test_http_parser_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing http-parser static libraries'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg

    @allure.title('http-parser-staticdev: minimal test')
    @pytest.mark.minimal
    def test_http_parser_static_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of http-parser-static (static library check)'''
        with allure.step('Check for static library file via GCC'):
            cmd = ssh_client.exec(
                'gcc -print-file-name=libhttp_parser.a', ignore_rc=True)
            assert cmd.rc == 0, \
                f"HTTP Parser Static failed (Static library libhttp_parser.a not found in GCC search path): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('http-parser-staticdev: compile and run simple C program')
    @pytest.mark.parametrize('are_utils_available', [['gcc', 'ldd']], indirect=True)
    def test_http_parser_compile(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that http_parser.h exists and libhttp_parser can be linked.
        Compiles a minimal C program using http_parser_init.
        '''
        source_path = f'{remote_tmp_path}/test_http.c'
        binary_path = f'{remote_tmp_path}/test_http_app'

        ssh_client.put_file(
            f'{test_files_path}/test_http.c', remote_tmp_path)

        lib_path = ''
        with allure.step('Locate static library path'):
            cmd = ssh_client.exec(
                'gcc -print-file-name=libhttp_parser.a', ignore_rc=True)
            if cmd.rc == 0 and '/' in cmd.stdout:
                lib_path = cmd.stdout.strip()
            else:
                lib_path = '-lhttp_parser'

        with allure.step(f'Compile with -static {lib_path}'):
            cmd = ssh_client.exec(
                f'gcc -static -o {binary_path} {source_path} {lib_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"HTTP Parser Static failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"HTTP Parser Static failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Parser initialized', cmd.stdout,
                        f"HTTP Parser Static failed (Parser was not initialized): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify binary does not use shared library'):
            cmd = ssh_client.exec(
                f'! ldd {binary_path} | grep libhttp_parser', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"HTTP Parser Static failed (Binary is dynamically linked, expected static): out='{cmd.stdout}', err='{cmd.stderr}'")
