import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib


@allure.suite('zlib-dev tests')
@pytest.mark.smoke
@pytest.mark.zlib_dev
class TestZlibDev:
    '''zlib-dev smoke test class'''

    @allure.title('zlib-dev: check headers')
    @pytest.mark.minimal
    def test_zlib_dev_headers(self, ssh_client: SshClient):
        '''Testing zlib headers installed'''
        with allure.step('Check zlib.h presence'):
            cmd = ssh_client.exec('test -f /usr/include/zlib.h', ignore_rc=True)
            assert cmd.rc == 0, f"zlib-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('zlib-dev: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libz.so'])
    def test_zlib_dev_shared_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing zlib shared libraries installed'''
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f"zlib-dev failed (shared library {lib} check failed) out='{msg}', err=''"

    @allure.title('zlib-dev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libz.a'])
    def test_zlib_dev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing zlib static libraries installed'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, f"zlib-dev failed (static library {lib} check failed) out='{msg}', err=''"

    # pylint: disable=unused-argument
    @allure.title('zlib-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_zlib_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing zlib basic workability via compilation'''
        ssh_client.put_file(f'{test_files_path}/test_zlib_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(
                f'g++ -o {remote_tmp_path}/zlib_test {remote_tmp_path}/test_zlib_dev.cpp -lz && {remote_tmp_path}/zlib_test',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"zlib-dev failed (compilation or execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"
