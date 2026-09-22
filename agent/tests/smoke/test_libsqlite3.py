import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libsqlite3 tests')
@pytest.mark.smoke
@pytest.mark.libsqlite3
class TestLibSqlite3Runtime:
    '''Tests covering the main libsqlite3 runtime package.'''

    @allure.title('libsqlite3: libraries test')
    @pytest.mark.minimal
    def test_libsqlite3_lib(self, ssh_client: SshClient):
        '''Test libsqlite3 libraries installed'''
        with allure.step('Checking libsqlite3 libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libsqlite3.so*')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libsqlite3: compile and run (dynamic linkage)')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libsqlite3_runtime_package(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies the main libsqlite3 package.
        Compiles a program dynamically (-lsqlite3) and runs it.
        '''
        source_path = f'{remote_tmp_path}/test_libsqlite3.c'
        binary_path = f'{remote_tmp_path}/test_libsqlite3_run'

        ssh_client.put_file(
            f'{test_files_path}/test_libsqlite3.c', remote_tmp_path)

        with allure.step('Compile dynamically with -lsqlite3'):
            cmd = ssh_client.exec(
                f'gcc {source_path} -o {binary_path} -lsqlite3', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libsqlite3 failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libsqlite3 failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('SQLite3 opened successfully', cmd.stdout,
                        f"Libsqlite3 failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
