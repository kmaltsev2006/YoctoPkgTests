import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('liburing-dev tests')
@pytest.mark.smoke
@pytest.mark.liburing_dev
class TestLiburingDev:
    '''liburing-dev smoke test class'''

    @allure.title('liburing-dev: headers presence')
    @pytest.mark.minimal
    def test_liburing_dev_headers(self, ssh_client: SshClient):
        '''Check that liburing headers are installed'''
        with allure.step('Checking liburing header presence'):
            cmd = ssh_client.exec(
                'test -f /usr/include/liburing.h',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'liburing-dev failed (header not found): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('liburing-dev: shared library presence')
    @pytest.mark.minimal
    def test_liburing_dev_library(self, ssh_client: SshClient):
        '''Check that liburing shared library is installed'''
        with allure.step('Checking liburing shared library ELF'):
            is_elf, msg = check_elf_file(
                ssh_client,
                '/usr/lib/liburing.so'
            )
            assert is_elf, f'liburing-dev failed (invalid ELF shared library): {msg}'

    # pylint: disable=unused-argument
    @allure.title('liburing-dev: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_liburing_dev_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile and run test program using liburing'''
        remote_source = f'{remote_tmp_path}/test_liburing.c'
        test_binary = f'{remote_tmp_path}/test_liburing'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_liburing.c',
                remote_source
            )

        with allure.step('Compiling test program'):
            cmd = ssh_client.exec(
                f'gcc -o {test_binary} {remote_source} -luring',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'liburing-dev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(cmd.rc, 0, f'liburing-dev failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"')
