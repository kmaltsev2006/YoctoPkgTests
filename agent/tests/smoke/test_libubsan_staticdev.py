import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libubsan-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libubsan_staticdev
class TestLibubsanStaticdev:
    '''libubsan-staticdev smoke test class'''

    @allure.title('libubsan-staticdev: check static library presence')
    @pytest.mark.minimal
    def test_libubsan_static_library(self, ssh_client: SshClient):
        '''Test that libubsan static library is installed'''
        with allure.step('Checking libubsan.a presence'):
            is_static, msg = check_static_lib(
                ssh_client,
                '/usr/lib/libubsan.a'
            )
            assert is_static, f'libubsan-staticdev failed (static lib check): err="{msg}"'

    # pylint: disable=unused-argument
    @allure.title('libubsan-staticdev: compile and run UBSan static test')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libubsan_staticdev_workability(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Test compiling and running UBSan test program with static library'''
        remote_source = f'{remote_tmp_path}/test_ubsan_error.c'
        test_binary = f'{remote_tmp_path}/test_ubsan_error'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_ubsan_error.c',
                remote_source
            )

        with allure.step('Compiling test program with static UBSan'):
            cmd = ssh_client.exec(
                'gcc -static -fsanitize=undefined '
                f'{remote_source} -o {test_binary}',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'libubsan-staticdev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running test program to trigger UBSan error'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.not_equal(
                cmd.rc,
                0,
                f'libubsan-staticdev failed (runtime should exit non-zero): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
