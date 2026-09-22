import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cracklib-dev tests')
@pytest.mark.smoke
@pytest.mark.cracklib_dev
class TestCracklibDev:
    '''cracklib-dev smoke tests'''

    @allure.title('cracklib-dev: header exists')
    @pytest.mark.minimal
    def test_header_exists(self, ssh_client: SshClient):
        '''Check that cracklib header file exists'''
        with allure.step('Verifying /usr/include/crack.h header'):
            cmd = ssh_client.exec('ls /usr/include/crack.h', ignore_rc=True)
            assert cmd.rc == 0, 'crack.h header is missing — cracklib-dev not installed'

    # pylint: disable=unused-argument
    @allure.title('cracklib-dev: run minimal program with strong password')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_run_minimal_cracklib(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Run minimal program with a strong password that passes FascistCheck'''
        with allure.step('Copy minimal C program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_cracklib_dev.c',
                f'{remote_tmp_path}/test_cracklib_dev.c'
            )

        with allure.step('Compiling and running the C program with libcrack'):
            cmd = ssh_client.exec(
                f'gcc {remote_tmp_path}/test_cracklib_dev.c -o {remote_tmp_path}/test_cracklib_dev '
                f'-lcrack && {remote_tmp_path}/test_cracklib_dev',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'Program failed: {cmd.stderr}'
