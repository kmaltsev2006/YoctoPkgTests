import pytest
import pytest_check as check
import allure
from helpers import check_elf_file
from cyp_test_lib.ssh_client import SshClient


@allure.suite('openssl-dev tests')
@pytest.mark.smoke
@pytest.mark.openssl_dev
class TestOpensslDev:
    '''openssl-dev smoke test class'''

    @allure.title('openssl-dev: headers presence')
    @pytest.mark.minimal
    def test_openssl_dev_headers(self, ssh_client: SshClient):
        '''Test that OpenSSL development headers are installed'''
        with allure.step('Checking /usr/include/openssl/ssl.h presence'):
            cmd = ssh_client.exec('ls /usr/include/openssl/ssl.h 2>/dev/null', ignore_rc=True)
            check.equal(
                cmd.rc,
                0,
                f'openssl-dev failed (headers presence): out="{cmd.stdout}", err="{cmd.stderr}"'
            )

    @allure.title('openssl-dev: shared library presence')
    @pytest.mark.minimal
    def test_openssl_dev_shared_library(self, ssh_client: SshClient):
        '''Test that OpenSSL shared library is installed'''
        with allure.step('Checking /usr/lib/libssl.so presence'):
            is_shared, msg = check_elf_file(ssh_client, '/usr/lib/libssl.so')
            check.is_true(
                is_shared,
                f'openssl-dev failed (shared library presence): out="{msg}"'
            )

    # pylint: disable=unused-argument
    @allure.title('openssl-dev: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_openssl_dev_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile and run test program linking against OpenSSL libraries'''
        remote_source = f'{remote_tmp_path}/test_openssl.c'
        test_binary = f'{remote_tmp_path}/test_openssl'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(f'{test_files_path}/test_openssl.c', remote_source)

        with allure.step('Compiling test program with -lssl -lcrypto'):
            cmd = ssh_client.exec(
                f'gcc {remote_source} -lssl -lcrypto -o {test_binary}',
                ignore_rc=True
            )
            check.equal(
                cmd.rc,
                0,
                f'openssl-dev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"'
            )

        with allure.step('Running compiled test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(
                cmd.rc,
                0,
                f'openssl-dev failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
            check.is_in(
                'OPENSSL_OK',
                cmd.stdout,
                f'openssl-dev failed (execution output): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
