import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('libgssglue-dev tests')
@pytest.mark.smoke
@pytest.mark.libgssglue_dev
class TestLibgssglueDev:
    '''libgssglue-dev smoke tests'''

    @allure.title('libgssglue-dev: header file exists')
    @pytest.mark.minimal
    def test_header_file_exists(self, ssh_client: SshClient):
        '''Test that libgssglue development header file exists'''
        with allure.step('Checking /usr/include/gssglue/gssapi/gssapi.h'):
            cmd = ssh_client.exec(
                'ls /usr/include/gssglue/gssapi/gssapi.h', ignore_rc=True)
            assert cmd.rc == 0, f'libgssglue-dev failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('libgssglue-dev: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_compile_and_run(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile and run test program using libgssglue library'''
        with allure.step('Copy test program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_libgssglue_dev.c',
                f'{remote_tmp_path}/test_libgssglue_dev.c'
            )

        with allure.step('Compile and run program with libgssglue'):
            cmd = ssh_client.exec(
                f'gcc {remote_tmp_path}/test_libgssglue_dev.c -o {remote_tmp_path}/test_libgssglue_dev \
                      -lgssglue && {remote_tmp_path}/test_libgssglue_dev',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'libgssglue-dev failed: out="{cmd.stdout}", err="{cmd.stderr}"'
