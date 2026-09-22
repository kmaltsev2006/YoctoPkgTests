import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('zlib tests')
@pytest.mark.smoke
@pytest.mark.zlib
class TestZlib:
    '''zlib smoke test class'''

    @allure.title('zlib: testing installed headers')
    @pytest.mark.minimal
    def test_zlib_headers(self, ssh_client: SshClient):
        '''Test zlib headers installed'''
        with allure.step('Checking zlib headers'):
            cmd = ssh_client.exec('stat /usr/include/zlib.h', ignore_rc=True)
            assert cmd.rc == 0, f"zlib failed (headers not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('zlib: testing installed libraries')
    @pytest.mark.minimal
    def test_zlib_libraries(self, ssh_client: SshClient):
        '''Test zlib shared libraries installed'''
        with allure.step('Checking library files'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libz.so')
            assert is_elf, f'zlib failed: {msg}'

    @allure.title('zlib: C program compression test')
    def test_zlib(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test zlib with C program'''

        ssh_client.put_file(
            f'{test_files_path}/test_zlib.c', remote_tmp_path)
        with allure.step('Compiling and running C program that uses zlib'):
            command = f'gcc {remote_tmp_path}/test_zlib.c -o {remote_tmp_path}/test_zlib -lz && {remote_tmp_path}/test_zlib'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'COMPRESSED' in cmd.stdout, f"zlib failed: out='{cmd.stdout}', err='{cmd.stderr}'"
