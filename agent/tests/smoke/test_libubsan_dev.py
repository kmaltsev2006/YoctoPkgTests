import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('libubsan-dev tests')
@pytest.mark.smoke
@pytest.mark.libubsan_dev
class TestLibubsanDev:
    '''libubsan-dev smoke test class'''

    @allure.title('libubsan-dev: sanitizer headers test')
    @pytest.mark.minimal
    def test_libubsan_dev_headers(self, ssh_client: SshClient):
        '''Test that libubsan development headers are installed'''
        with allure.step('Checking sanitizer headers'):
            cmd = ssh_client.exec(
                'find /usr/include /usr/lib/gcc -name ubsan_interface.h',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'libubsan-dev failed (headers not found): out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=duplicate-code
    # pylint: disable=unused-argument
    @allure.title('libubsan-dev: UBSan runtime error detection test')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libubsan_dev_runtime(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Test that UBSan detects undefined behavior at runtime'''
        remote_source = f'{remote_tmp_path}/test_ubsan_error.c'
        test_binary = f'{remote_tmp_path}/test_ubsan_error'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_ubsan_error.c',
                remote_source
            )

        with allure.step('Compiling test program with UBSan enabled'):
            cmd = ssh_client.exec(
                f'gcc -fsanitize=undefined {remote_source} -o {test_binary}',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'libubsan-dev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running program to trigger undefined behavior'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.not_equal(
                cmd.rc,
                0,
                f'libubsan-dev failed (runtime should exit non-zero): out="{cmd.stdout}", err="{cmd.stderr}"'
            )

        with allure.step('Checking UBSan runtime error message'):
            check.is_in(
                'runtime error',
                cmd.stderr.lower(),
                f'libubsan-dev failed (UBSan error message not found): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
