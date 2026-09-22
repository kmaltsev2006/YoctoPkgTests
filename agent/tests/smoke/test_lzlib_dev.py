import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('lzlib-dev tests')
@pytest.mark.smoke
@pytest.mark.lzlib_dev
class TestLzlibDev:
    '''Tests covering lzlib-dev package.'''

    @allure.title('lzlib-dev: libraries test')
    @pytest.mark.minimal
    def test_lzlib_dev_lib(self, ssh_client: SshClient):
        '''Test lzlib-dev libraries installed'''
        with allure.step('Checking lzlib-dev libraries'):
            # lzlib libraries are usually named liblz.so
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblz.so')
            assert is_elf, msg

    @allure.title('lzlib-dev: headers test')
    @pytest.mark.minimal
    def test_lzlib_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/lzlib.h', ignore_rc=True)
            assert cmd.rc == 0, f"Lzlib-dev failed (Header file 'lzlib.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('lzlib-dev: compile and run')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_lzlib_dev_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Main test: Verifies that we can compile and run a program linking against lzlib.
        Command: gcc test.c -llz -o test
        '''
        source_path = f'{remote_tmp_path}/test_lzlib.c'
        binary_path = f'{remote_tmp_path}/test_lzlib_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_lzlib.c', remote_tmp_path)

        with allure.step('Compile dynamically with -llz'):
            cmd = ssh_client.exec(
                f'gcc {source_path} -o {binary_path} -llz', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Lzlib-dev failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Lzlib-dev failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('lzlib version:', cmd.stdout,
                        f"Lzlib-dev failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
