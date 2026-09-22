import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file
import pytest_check as check


@allure.suite('libasan-dev tests')
@pytest.mark.smoke
@pytest.mark.libasan_dev
class TestLibasanDev:
    '''libasan-dev smoke test class'''

    @allure.title('libasan-dev: libraries test')
    @pytest.mark.minimal
    def test_libasan_dev_lib(self, ssh_client: SshClient):
        '''Test libasan-dev libraries installed'''
        with allure.step('Checking libasan-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libasan.so')
            assert is_elf, f'libasan-dev failed: {msg}'

    @allure.title('libasan-dev: functional test')
    def test_libasan_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing compilation with ASAN'''
        ssh_client.put_file(
            f'{test_files_path}/asan_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/asan_test.c'
        test_binary = f'{remote_tmp_path}/asan_test'

        with allure.step('Compiling with ASAN flags'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -fsanitize=address',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f"libasan-dev failed (compile error): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Running ASAN program'):
            cmd = ssh_client.exec(
                f'ASAN_OPTIONS=detect_leaks=0 {test_binary}',
                ignore_rc=True
            )
            check.is_in('ASAN_COMPILATION_WORKS', cmd.stdout,
                        f"libasan-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'")
