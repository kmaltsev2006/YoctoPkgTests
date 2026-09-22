import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libsodium tests')
@pytest.mark.smoke
@pytest.mark.libsodium
class TestLibSodiumRuntime:
    '''Tests covering the main libsodium runtime package.'''

    @allure.title('libsodium: libraries test')
    @pytest.mark.minimal
    def test_libsodium_lib(self, ssh_client: SshClient):
        '''Test libsodium libraries installed'''
        with allure.step('Checking libsodium libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libsodium.so*')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libsodium: compile and run (dynamic linkage)')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libsodium_runtime_package(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies the main libsodium package.
        Compiles a program dynamically (-lsodium) and runs it.
        '''
        source_path = f'{remote_tmp_path}/test_libsodium.c'
        binary_path = f'{remote_tmp_path}/test_libsodium_run'

        ssh_client.put_file(
            f'{test_files_path}/test_libsodium.c', remote_tmp_path)

        with allure.step('Compile dynamically with -lsodium'):
            cmd = ssh_client.exec(
                f'gcc {source_path} -o {binary_path} -lsodium', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libsodium failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libsodium failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('Libsodium initialized', cmd.stdout,
                        f"Libsodium failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
