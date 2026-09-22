import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libkmod tests')
@pytest.mark.smoke
@pytest.mark.libkmod
class TestLibKmod:
    '''Tests for the libkmod library.'''

    @allure.title('libkmod: libraries test')
    @pytest.mark.minimal
    def test_libkmod_lib(self, ssh_client: SshClient):
        '''Test libkmod libraries installed'''
        with allure.step('Checking libkmod libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libkmod.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libkmod: compile and run context creation')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libkmod_compilation_and_run(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that a C program linking against libkmod compiles and runs correctly.
        '''
        source_path = f'{remote_tmp_path}/test_libkmod.c'
        binary_path = f'{remote_tmp_path}/test_kmod_app'

        ssh_client.put_file(
            f'{test_files_path}/test_libkmod.c', remote_tmp_path)

        with allure.step('Compile the C program linking libkmod'):
            cmd = ssh_client.exec(f'gcc {source_path} -o {binary_path} -lkmod', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libkmod failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libkmod failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('kmod context initialized successfully', cmd.stdout,
                        f"Libkmod failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
