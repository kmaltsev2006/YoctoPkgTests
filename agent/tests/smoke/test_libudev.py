import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libudev tests')
@pytest.mark.smoke
@pytest.mark.libudev
class TestLibudev:
    '''libudev smoke test class'''

    @allure.title('libudev: headers presence test')
    @pytest.mark.minimal
    def test_libudev_headers(self, ssh_client: SshClient):
        '''Test that libudev headers are installed'''
        with allure.step('Checking libudev headers'):
            cmd = ssh_client.exec(
                'test -f /usr/include/libudev.h',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'libudev failed (header check): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('libudev: shared library presence test')
    @pytest.mark.minimal
    def test_libudev_library(self, ssh_client: SshClient):
        '''Test that libudev shared library is installed'''
        with allure.step('Checking libudev shared library'):
            is_elf, msg = check_elf_file(
                ssh_client,
                '/usr/lib/libudev.so'
            )
            assert is_elf, f'libudev failed (shared library ELF check): err="{msg}"'

    # pylint: disable=unused-argument
    @allure.title('libudev: compile and run basic udev program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libudev_compile_and_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Test basic libudev usage: create udev context'''
        remote_source = f'{remote_tmp_path}/test_libudev.c'
        test_binary = f'{remote_tmp_path}/test_libudev'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_libudev.c',
                remote_source
            )

        with allure.step('Compiling libudev test program'):
            cmd = ssh_client.exec(
                f'gcc {remote_source} -o {test_binary} -ludev',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'libudev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running libudev test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(
                cmd.rc,
                0,
                f'libudev failed (runtime): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
            check.is_in(
                'UDEV_OK',
                cmd.stdout,
                f'libudev failed (unexpected output): out="{cmd.stdout}"'
            )
