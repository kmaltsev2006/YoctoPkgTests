import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gcc tests')
@pytest.mark.smoke
@pytest.mark.gcc
class TestGcc:
    '''gcc smoke test class'''
    @allure.title('gcc: compile test')
    @pytest.mark.minimal
    def test_gcc(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str ):
        '''Tests gcc compilation and running'''

        ssh_client.put_file(
                f'{test_files_path}/test_gcc.c', remote_tmp_path)

        command = f"gcc {remote_tmp_path}/test_gcc.c -o {remote_tmp_path}/test_gcc && {remote_tmp_path}/test_gcc"
        cmd = ssh_client.exec(command, ignore_rc=True)
        check.equal(
            cmd.rc, 0, f"Gcc failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        check.is_in('Hello!', cmd.stdout, f"Gcc failed (Unexpected output): out='{cmd.stdout}', err='{cmd.stderr}")
