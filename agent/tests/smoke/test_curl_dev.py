import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('curl-dev tests')
@pytest.mark.smoke
@pytest.mark.curl_dev
class TestCurlDev:
    '''curl-dev smoke tests'''

    @allure.title('curl-dev: header exists')
    @pytest.mark.minimal
    def test_header_exists(self, ssh_client: SshClient):
        '''Check that libcurl header exists'''
        with allure.step('Verifying presence of /usr/include/curl/curl.h'):
            cmd = ssh_client.exec('ls /usr/include/curl/curl.h', ignore_rc=True)
            assert cmd.rc == 0, 'curl.h header is missing — curl-dev not installed'

    # pylint: disable=unused-argument
    @allure.title('curl-dev: compile and run minimal program linking with libcurl')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_compile_minimal_curl(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile minimal program and verify it links with libcurl'''
        with allure.step('Copy minimal C program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_curl_dev.c',
                f'{remote_tmp_path}/test_curl_dev.c'
            )

        with allure.step('Compiling and running the C program with -lcurl'):
            cmd = ssh_client.exec(
                f'gcc {remote_tmp_path}/test_curl_dev.c -o {remote_tmp_path}/test_curl_dev -lcurl && {remote_tmp_path}/test_curl_dev',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'Program failed: {cmd.stderr}'
