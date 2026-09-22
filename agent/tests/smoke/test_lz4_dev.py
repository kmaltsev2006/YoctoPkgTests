import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib


@allure.suite('lz4-dev tests')
@pytest.mark.smoke
@pytest.mark.lz4_dev
class TestLz4Dev:
    '''Tests covering lz4-dev package (headers and dynamic link).'''

    @allure.title('lz4-dev: libraries test')
    @pytest.mark.minimal
    def test_lz4_dev_lib(self, ssh_client: SshClient):
        '''Test lz4-dev libraries installed'''
        with allure.step('Checking lz4-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblz4.so')
            assert is_elf, msg

    @allure.title('lz4-dev: headers test')
    @pytest.mark.minimal
    def test_lz4_dev_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/lz4.h', ignore_rc=True)
            assert cmd.rc == 0, f"Lz4-dev failed (Header file 'lz4.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('lz4-dev: compile and run (dynamic linkage)')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_lz4_dev_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Main test: Verifies that we can compile and run a program linking against lz4.
        '''
        source_path = f'{remote_tmp_path}/test_lz4.c'
        binary_path = f'{remote_tmp_path}/test_lz4_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_lz4.c', remote_tmp_path)

        with allure.step('Compile dynamically with -llz4'):
            cmd = ssh_client.exec(
                f'gcc {source_path} -o {binary_path} -llz4', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Lz4-dev failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Lz4-dev failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('LZ4 Version:', cmd.stdout,
                        f"Lz4-dev failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
