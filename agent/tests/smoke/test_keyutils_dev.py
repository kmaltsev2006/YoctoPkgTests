import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('keyutils-dev tests')
@pytest.mark.smoke
@pytest.mark.keyutils_dev
class TestKeyutilsDev:
    '''keyutils-dev smoke test class'''

    @allure.title('keyutils-dev: headers test')
    @pytest.mark.minimal
    def test_keyutils_dev_headers(self, ssh_client: SshClient):
        '''Test keyutils-dev headers installed'''
        with allure.step('Checking keyutils-dev headers'):
            cmd = ssh_client.exec(
                'stat /usr/include/keyutils.h', ignore_rc=True)
            assert cmd.rc == 0, f"keyutils-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('keyutils-dev: libraries test')
    @pytest.mark.minimal
    def test_keyutils_dev_lib(self, ssh_client: SshClient):
        '''Test keyutils-dev libraries installed'''
        with allure.step('Checking keyutils-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libkeyutils.so')
            assert is_elf, f'keyutils-dev failed: {msg}'

    @allure.title('keyutils-dev: compile and link test')
    def test_keyutils_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libkeyutils'''

        ssh_client.put_file(
            f'{test_files_path}/keyutils_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/keyutils_test.c'
        test_binary = f'{remote_tmp_path}/keyutils_test'

        with allure.step('Compiling and running test program'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -lkeyutils && {test_binary}', ignore_rc=True
            )
            # The test might fail if kernel doesn't support keyrings, check for compilation success
            assert cmd.rc == 0 and 'KEYUTILS_FUNCTIONS_WORK' in cmd.stdout, f"keyutils-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
