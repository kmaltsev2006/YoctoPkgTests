import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtsan-dev tests')
@pytest.mark.smoke
@pytest.mark.libtsan_dev
class TestLibtsanDev:
    '''libtsan-dev smoke test class'''

    @allure.title('libtsan-dev: libraries test')
    @pytest.mark.minimal
    def test_libtsan_dev_lib(self, ssh_client: SshClient):
        '''Test libtsan-dev libraries installed'''
        with allure.step('Checking libtsan-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libtsan.so')
            assert is_elf, f'libtsan-dev failed: {msg}'

    @allure.title('libtsan-dev: compile with TSAN test')
    def test_libtsan_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing compilation with TSAN'''
        ssh_client.put_file(
            f'{test_files_path}/tsan_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/tsan_test.c'
        test_binary = f'{remote_tmp_path}/tsan_test'

        with allure.step('Compiling with TSAN flags'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -fsanitize=thread -lpthread && {test_binary}',
                ignore_rc=True
            )
            output = cmd.stdout.lower() + cmd.stderr.lower()
            assert cmd.rc == 0 or (cmd.rc != 127 and (
                'warning' in output or 'data race' in output)), f"libtsan-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
