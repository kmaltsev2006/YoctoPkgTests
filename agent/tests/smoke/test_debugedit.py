import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('debugedit tests')
@pytest.mark.smoke
@pytest.mark.debugedit
class TestDebugedit:
    '''Tests for the debugedit utility package'''

    @allure.title('debugedit: minimal test')
    @pytest.mark.minimal
    def test_debugedit_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of debugedit'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('debugedit --version', ignore_rc=True)
            assert cmd.rc == 0, f"Debugedit failed (Debugedit is not installed): out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('debugedit: replaces source path in debug info')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_debugedit_replaces_path(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests that `debugedit` successfully finds and replaces the compilation
        source path within the executable's debug information.
        '''

        ssh_client.put_file(
            f'{test_files_path}/test_debugedit_hello.cpp', remote_tmp_path)

        original_source_path = f'{remote_tmp_path}/test_debugedit_hello.cpp'
        binary_path = f'{remote_tmp_path}/test_debugedit_hello_binary'

        original_base_path = f'{remote_tmp_path}'
        new_base_path = '/usr/src/debug/my-test-project'
        new_full_path = f'{new_base_path}/test_debugedit_hello.cpp'

        with allure.step(f"Compiling source file with debug info to {binary_path}"):
            compile_cmd = f"g++ -g -o {binary_path} {original_source_path}"
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Debugedit failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step(f"Verify original path '{original_source_path}' exists"):
            cmd = ssh_client.exec(
                f'strings {binary_path} | grep -q {original_source_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Debugedit failed (Original path was not found before running debugedit): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step(f"Run debugedit to replace '{original_base_path}' with '{new_base_path}'"):
            cmd = ssh_client.exec(
                f'debugedit -b {original_base_path} -d {new_base_path} {binary_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Debugedit failed (Debugedit execution failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step(f"Verify original path '{original_source_path}' is gone"):
            cmd = ssh_client.exec(
                f'! strings {binary_path} | grep -q {original_source_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Debugedit failed (Original path still exists after running debugedit): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step(f"Verify new path '{new_full_path}' exists"):
            cmd = ssh_client.exec(
                f'strings {binary_path} | grep -q {new_full_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Debugedit failed (New path was not found after running debugedit): out='{cmd.stdout}', err='{cmd.stderr}")
