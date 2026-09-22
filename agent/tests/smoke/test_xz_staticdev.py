import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('xz-staticdev tests')
@pytest.mark.smoke
@pytest.mark.xz_staticdev
class TestXzStaticdev:
    '''xz-staticdev smoke tests'''

    @allure.title('xz-staticdev: header file exists')
    @pytest.mark.minimal
    def test_header_file_exists(self, ssh_client: SshClient):
        '''Test that xz development header file exists'''
        with allure.step('Checking /usr/include/lzma.h'):
            cmd = ssh_client.exec('ls /usr/include/lzma.h', ignore_rc=True)
            assert cmd.rc == 0, f'xz-staticdev failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('xz-staticdev: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_compile_and_run(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile and run test program using xz library'''
        with allure.step('Copy test program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_xz_staticdev.c',
                f'{remote_tmp_path}/test_xz_staticdev.c'
            )

        with allure.step('Compile and run program with liblzma'):
            cmd = ssh_client.exec(
                f'gcc {remote_tmp_path}/test_xz_staticdev.c -o {remote_tmp_path}/test_xz_staticdev -llzma && {remote_tmp_path}/test_xz_staticdev',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'xz-staticdev failed: out="{cmd.stdout}", err="{cmd.stderr}"'
