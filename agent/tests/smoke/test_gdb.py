import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gdb tests')
@pytest.mark.smoke
@pytest.mark.gdb
class TestGdb:
    '''gdb smoke tests'''

    @allure.title('gdb: binary exists')
    @pytest.mark.minimal
    def test_gdb_binary_exists(self, ssh_client: SshClient):
        '''Check that gdb binary exists in /usr/bin'''
        with allure.step('Verifying /usr/bin/gdb binary'):
            cmd = ssh_client.exec('ls /usr/bin/gdb', ignore_rc=True)
            assert cmd.rc == 0, 'gdb binary is missing — gdb not installed'

    @allure.title('gdb: print version')
    @pytest.mark.minimal
    def test_gdb_version(self, ssh_client: SshClient):
        '''Check that gdb runs and prints version'''
        with allure.step('Running gdb --version'):
            cmd = ssh_client.exec('gdb --version', ignore_rc=True)
            check.equal(cmd.rc, 0, f'gdb failed to run: {cmd.stderr}')
            check.is_in('GNU gdb', cmd.stdout,
                        f'Unexpected gdb version output: {cmd.stdout}')

    # pylint: disable=unused-argument
    @allure.title('gdb: run minimal program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_gdb_run_minimal_program(self, ssh_client: SshClient, remote_tmp_path: str, are_utils_available: None):
        '''Compile and run a minimal program under gdb to verify basic functionality'''

        with allure.step(f'Creating minimal C program {remote_tmp_path}/test_gdb.c'):
            ssh_client.exec(
                'echo "#include <stdio.h>\nint main() { printf(\\"Hello, GDB!\\n\\"); return 0; }" '
                f'> {remote_tmp_path}/test_gdb.c'
            )

        with allure.step('Compiling minimal C program'):
            cmd = ssh_client.exec(
                f'gcc {remote_tmp_path}/test_gdb.c -o {remote_tmp_path}/test_gdb',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'Compilation failed: {cmd.stderr}')

        with allure.step('Running program under gdb non-interactively'):
            cmd = ssh_client.exec(
                f'gdb -batch -ex run -ex quit {remote_tmp_path}/test_gdb',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'Program failed under gdb: {cmd.stderr}')
            check.is_in('Hello, GDB!', cmd.stdout,
                        f'Unexpected program output: {cmd.stdout}')
