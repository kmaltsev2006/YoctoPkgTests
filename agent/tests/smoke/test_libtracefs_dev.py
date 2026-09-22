import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtracefs-dev tests')
@pytest.mark.smoke
@pytest.mark.libtracefs_dev
class TestLibtracefsDev:
    '''libtracefs-dev smoke test class'''

    @allure.title('libtracefs-dev: headers test')
    @pytest.mark.minimal
    def test_libtracefs_dev_headers(self, ssh_client: SshClient):
        '''Test libtracefs-dev headers installed'''
        with allure.step('Checking libtracefs-dev headers'):
            cmd = ssh_client.exec(
                'stat /usr/include/tracefs.h',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"libtracefs-dev failed (headers not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libtracefs-dev: libraries test')
    @pytest.mark.minimal
    def test_libtracefs_dev_lib(self, ssh_client: SshClient):
        '''Test libtracefs-dev libraries installed'''
        with allure.step('Checking libtracefs-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libtracefs.so')
            assert is_elf, f'libtracefs-dev failed: {msg}'

    @allure.title('libtracefs-dev: compile and link test')
    def test_libtracefs_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libtracefs'''
        ssh_client.put_file(
            f'{test_files_path}/libtracefs_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libtracefs_test.c'
        test_binary = f'{remote_tmp_path}/libtracefs_test'

        with allure.step('Compiling and running with libtracefs'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -ltracefs -I /usr/include/traceevent && {test_binary}',
                ignore_rc=True
            )
            success_conditions = [
                'TRACEFS_FOUND',
                'LIBTRACEFS_TEST_PASS'
            ]

            success = any(
                condition in cmd.stdout for condition in success_conditions)
            assert cmd.rc == 0 and success, f"libtracefs-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
