import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('fmt-staticdev tests')
@pytest.mark.smoke
@pytest.mark.fmt_staticdev
class TestFmtStaticdev:
    '''fmt-staticdev smoke test class'''

    @allure.title('fmt-staticdev: check headers')
    @pytest.mark.minimal
    def test_fmt_staticdev_headers(self, ssh_client: SshClient):
        '''Check fmt-staticdev headers'''
        with allure.step('Check fmt-staticdev headers'):
            cmd = ssh_client.exec('test -e /usr/include/fmt', ignore_rc=True)
            assert cmd.rc == 0, f'fmt headers not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=duplicate-code
    @allure.title('fmt-staticdev: check static libraries')
    @pytest.mark.minimal
    def test_fmt_staticdev_static_libraries(self, ssh_client: SshClient):
        '''Check fmt-staticdev static libraries'''
        with allure.step('Check libfmt.a'):
            is_static_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libfmt.a')
            assert is_static_lib, f'fmt static library check failed: out="{msg}", err=""'

    # pylint: disable=duplicate-code
    # pylint: disable=unused-argument
    @allure.title('fmt-staticdev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_fmt_staticdev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Check fmt-staticdev workability'''

        with allure.step('Copy test_fmt.cpp to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_fmt.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(
                f'g++ -o {remote_tmp_path}/a.out {remote_tmp_path}/test_fmt.cpp -lfmt && {remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'fmt-staticdev is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
