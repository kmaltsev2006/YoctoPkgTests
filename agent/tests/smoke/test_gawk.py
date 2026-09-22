import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gawk tests')
@pytest.mark.smoke
@pytest.mark.gawk
class TestBison:
    '''gawk smoke test class'''

    @allure.title('gawk: check installation')
    @pytest.mark.minimal
    def test_gawk_installation(self, ssh_client: SshClient):
        with allure.step('Check gawk installation'):
            cmd = ssh_client.exec('which gawk', ignore_rc=True)
            assert cmd.rc == 0, f'gawk not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('gawk: check workability')
    @pytest.mark.minimal
    def test_gawk_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy test_gawk.txt to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_gawk.txt', remote_tmp_path)
        with allure.step('Compile'):
            cmd = ssh_client.exec(
                f"gawk '{{print}}' {remote_tmp_path}/test_gawk.txt", ignore_rc=True)
            assert cmd.rc == 0 and cmd.stdout == 'lorem ipsum dolor sit amet', f'gawk is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
