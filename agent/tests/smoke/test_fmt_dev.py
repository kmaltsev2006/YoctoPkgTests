import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib


@allure.suite('fmt-dev tests')
@pytest.mark.smoke
@pytest.mark.fmt_dev
class TestFmtDev:
    '''fmt-dev smoke test class'''

    @allure.title('fmt-dev: check headers')
    @pytest.mark.minimal
    def test_fmt_dev_headers(self, ssh_client: SshClient):
        '''Check fmt-dev headers'''
        with allure.step('Check fmt-dev headers'):
            cmd = ssh_client.exec('test -e /usr/include/fmt', ignore_rc=True)
            assert cmd.rc == 0, f'fmt headers not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('fmt-dev: check shared libraries')
    @pytest.mark.minimal
    def test_fmt_dev_shared_libraries(self, ssh_client: SshClient):
        '''Check fmt-dev shared libraries'''
        with allure.step('Check libfmt.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libfmt.so')
            assert is_elf, f'fmt shared library check failed: out="{msg}", err=""'

    # pylint: disable=duplicate-code
    @allure.title('fmt-dev: check static libraries')
    @pytest.mark.minimal
    def test_fmt_dev_static_libraries(self, ssh_client: SshClient):
        '''Check fmt-dev static libraries'''
        with allure.step('Check libfmt.a'):
            is_static_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libfmt.a')
            assert is_static_lib, f'fmt static library check failed: out="{msg}", err=""'

    # pylint: disable=duplicate-code
    # pylint: disable=unused-argument
    @allure.title('fmt-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_fmt_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Check fmt-dev workability'''
        with allure.step('Copy test_fmt.cpp to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_fmt.cpp', remote_tmp_path)
        with allure.step('Compile and run'):
            cmd = ssh_client.exec(
                f'g++ -o {remote_tmp_path}/a.out {remote_tmp_path}/test_fmt.cpp -lfmt && {remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'fmt-dev is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
