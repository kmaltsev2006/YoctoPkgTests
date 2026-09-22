import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('libunwind-dev tests')
@pytest.mark.smoke
@pytest.mark.libunwind_dev
class TestLibunwindDev:
    '''libunwind-dev smoke test class'''

    @allure.title('libunwind-dev: headers presence test')
    @pytest.mark.minimal
    def test_libunwind_dev_headers(self, ssh_client: SshClient):
        '''Test that libunwind development headers are installed'''
        with allure.step('Checking libunwind headers in standard include paths'):
            cmd = ssh_client.exec(
                'ls /usr/include/libunwind.h',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'libunwind failed (header check): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('libunwind-dev: pkg-config file presence test')
    @pytest.mark.minimal
    def test_libunwind_dev_pkgconfig(self, ssh_client: SshClient):
        '''Test that libunwind pkg-config file is installed'''
        with allure.step('Checking libunwind pkg-config file'):
            cmd = ssh_client.exec(
                'pkg-config --exists libunwind',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'libunwind failed (pkg-config check): out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('libunwind-dev: compile and run unwind test')
    @pytest.mark.parametrize('are_utils_available', [['gcc', 'pkg-config']], indirect=True)
    def test_libunwind_dev_compile_and_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Test compilation and execution using libunwind'''
        remote_source = f'{remote_tmp_path}/test_libunwind.c'
        test_binary = f'{remote_tmp_path}/test_libunwind'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_libunwind.c',
                remote_source
            )

        with allure.step('Compiling libunwind test program'):
            cmd = ssh_client.exec(
                f'gcc {remote_source} -o {test_binary} '
                f'-lunwind -lunwind-x86_64',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'libunwind failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running libunwind test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(cmd.rc, 0, f'libunwind failed (runtime): out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_in('UNWIND_OK', cmd.stdout, f'libunwind failed (unexpected output): out="{cmd.stdout}"')
