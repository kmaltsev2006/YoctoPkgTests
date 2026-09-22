import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('curl-staticdev tests')
@pytest.mark.smoke
@pytest.mark.curl_staticdev
class TestCurlStaticDev:
    '''curl-staticdev smoke tests'''

    @allure.title('curl-staticdev: static library exists')
    @pytest.mark.minimal
    def test_curl_static_lib_exists(self, ssh_client: SshClient):
        '''Verify that libcurl.a is present'''
        with allure.step('Checking /usr/lib/libcurl.a'):
            cmd = ssh_client.exec('test -f /usr/lib/libcurl.a', ignore_rc=True)
            assert cmd.rc == 0, cmd.stderr

    # pylint: disable=unused-argument
    @allure.title('curl-staticdev: compile minimal static program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_compile_static_curl(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile and link a minimal program statically with libcurl'''
        with allure.step('Copy minimal C program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_curl_staticdev.c',
                f'{remote_tmp_path}/test_curl_staticdev.c'
            )

        with allure.step('Compiling the program statically with libcurl'):
            cmd = ssh_client.exec(
                f'gcc {remote_tmp_path}/test_curl_staticdev.c -o {remote_tmp_path}/test_curl_staticdev -lcurl -static',
                ignore_rc=True
            )
            assert cmd.rc == 0, cmd.stderr
