import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libarchive-dev tests')
@pytest.mark.smoke
@pytest.mark.libarchive_dev
class TestLibarchiveDev:
    '''libarchive-dev smoke test class'''

    @allure.title('libarchive-dev: headers test')
    @pytest.mark.minimal
    def test_libarchive_dev_headers(self, ssh_client: SshClient):
        '''Test libarchive-dev headers installed'''
        with allure.step('Checking libarchive-dev headers'):
            cmd = ssh_client.exec(
                'stat /usr/include/archive.h', ignore_rc=True)
            assert cmd.rc == 0, f"libarchive-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libarchive-dev: libraries test')
    @pytest.mark.minimal
    def test_libarchive_dev_lib(self, ssh_client: SshClient):
        '''Test libarchive-dev libraries installed'''
        with allure.step('Checking libarchive-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libarchive.so')
            assert is_elf, f'libarchive-dev failed: {msg}'

    @allure.title('libarchive-dev: functional test')
    def test_libarchive_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libarchive'''
        ssh_client.put_file(
            f'{test_files_path}/libarchive_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libarchive_test.c'
        test_binary = f'{remote_tmp_path}/libarchive_test'

        with allure.step('Compiling and running test program'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -larchive && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBARCHIVE_FUNCTIONS_WORK' in cmd.stdout, \
                f"libarchive-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
