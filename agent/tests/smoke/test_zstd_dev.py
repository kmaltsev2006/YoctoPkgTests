import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('zstd-dev tests')
@pytest.mark.smoke
@pytest.mark.zstd_dev
class TestZstdDev:
    '''zstd-dev smoke test class'''

    @allure.title('zstd-dev: check headers')
    @pytest.mark.minimal
    def test_zstd_dev_headers(self, ssh_client: SshClient):
        '''Testing zstd headers installed'''
        with allure.step('Check zstd.h presence'):
            cmd = ssh_client.exec('test -f /usr/include/zstd.h', ignore_rc=True)
            assert cmd.rc == 0, f"zstd-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('zstd-dev: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libzstd.so'])
    def test_zstd_dev_shared_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing zstd shared libraries installed'''
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f"zstd-dev failed (shared library {lib} check failed) out='{msg}', err=''"

    # pylint: disable=unused-argument
    @allure.title('zstd-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_zstd_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing zstd basic workability via compilation'''
        ssh_client.put_file(f'{test_files_path}/test_zstd_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(
                f'g++ -o {remote_tmp_path}/zstd_test {remote_tmp_path}/test_zstd_dev.cpp -lzstd && {remote_tmp_path}/zstd_test',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"zstd-dev failed (compilation or execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"
