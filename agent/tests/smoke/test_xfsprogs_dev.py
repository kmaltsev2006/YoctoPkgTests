import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib


@allure.suite('xfsprogs-dev tests')
@pytest.mark.smoke
@pytest.mark.xfsprogs_dev
class TestXfsprogsDev:
    '''xfsprogs-dev smoke test class'''

    @allure.title('xfsprogs-dev: check headers')
    @pytest.mark.minimal
    def test_xfsprogs_dev_headers(self, ssh_client: SshClient):
        '''Testing xfsprogs headers installed'''
        with allure.step('Check xfs headers'):
            cmd = ssh_client.exec('test -e /usr/include/xfs/xfs.h', ignore_rc=True)
            assert cmd.rc == 0, f"xfsprogs-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('xfsprogs-dev: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libhandle.so'])
    def test_xfsprogs_dev_shared_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing xfsprogs shared libraries installed'''
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f"xfsprogs-dev failed (shared library {lib} check failed) out='{msg}', err=''"

    @allure.title('xfsprogs-dev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libhandle.a'])
    def test_xfsprogs_dev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing xfsprogs static libraries installed'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, f"xfsprogs-dev failed (static library {lib} check failed) out='{msg}', err=''"

    # pylint: disable=unused-argument
    @allure.title('xfsprogs-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_xfsprogs_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing xfsprogs-dev basic workability via compilation'''
        ssh_client.put_file(f'{test_files_path}/test_xfsprogs_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            # Link against libhandle
            cmd = ssh_client.exec(
                f'g++ -o {remote_tmp_path}/xfs_test {remote_tmp_path}/test_xfsprogs_dev.cpp -lhandle && '
                f'{remote_tmp_path}/xfs_test',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"xfsprogs-dev failed (compilation or execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"
