import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cups-dev tests')
@pytest.mark.smoke
@pytest.mark.cups_dev
class TestCupsDev:
    '''cups-dev smoke tests'''

    @allure.title('cups-dev: header exists')
    @pytest.mark.minimal
    def test_header_exists(self, ssh_client: SshClient):
        '''Check that cups.h header exists'''
        with allure.step('Checking /usr/include/cups/cups.h'):
            cmd = ssh_client.exec('ls /usr/include/cups/cups.h', ignore_rc=True)
            assert cmd.rc == 0, 'cups.h header is missing — cups-dev not installed'

    # pylint: disable=unused-argument
    @allure.title('cups-dev: compile minimal program using libcups function')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_compile_minimal_cups(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile minimal C program using CUPS library'''
        with allure.step('Copy minimal C program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_cups_dev.c',
                f'{remote_tmp_path}/test_cups_dev.c'
            )

        with allure.step('Compiling and running program with libcups'):
            cmd = ssh_client.exec(
                f'gcc {remote_tmp_path}/test_cups_dev.c -o {remote_tmp_path}/test_cups_dev -lcups && {remote_tmp_path}/test_cups_dev',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'Program failed: {cmd.stderr}'
