import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

LIBCRYPT_STATIC = 'libcrypt.a'
LIBCRYPT_SHARED = 'libcrypt.so'


@allure.suite('libxcrypt-compat tests')
@pytest.mark.smoke
@pytest.mark.libxcrypt_compat
class TestLibxcryptCompat:
    '''libxcrypt-compat smoke test class'''

    @allure.title('libxcrypt-compat: headers presence')
    @pytest.mark.minimal
    def test_libxcrypt_headers(self, ssh_client: SshClient):
        '''Check that libcrypt header is installed'''
        with allure.step('Checking /usr/include/crypt.h presence'):
            cmd = ssh_client.exec('test -f /usr/include/crypt.h', ignore_rc=True)
            assert cmd.rc == 0, f'libxcrypt-compat failed (header missing): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('libxcrypt-compat: shared library presence')
    @pytest.mark.minimal
    def test_libxcrypt_shared_library(self, ssh_client: SshClient):
        '''Check that libcrypt shared library is installed'''
        with allure.step(f'Checking /usr/lib/{LIBCRYPT_SHARED} presence'):
            is_shared, msg = check_elf_file(ssh_client, f'/usr/lib/{LIBCRYPT_SHARED}')
            assert is_shared, f'libxcrypt-compat failed (shared library invalid): {msg}'

    # pylint: disable=unused-argument
    @allure.title('libxcrypt-compat: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libxcrypt_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile and run a small C program linking against libcrypt'''
        remote_source = f'{remote_tmp_path}/test_libxcrypt.c'
        binary_path = f'{remote_tmp_path}/test_libxcrypt'

        with allure.step('Copying test source to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_libxcrypt.c',
                remote_source
            )

        with allure.step('Compiling test program'):
            cmd = ssh_client.exec(
                f'gcc -o {binary_path} {remote_source} -lcrypt',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'libxcrypt-compat failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running test program'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f'libxcrypt-compat failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_in('CRYPT_OK', cmd.stdout, f'libxcrypt-compat failed (wrong output): out="{cmd.stdout}", err="{cmd.stderr}"')
