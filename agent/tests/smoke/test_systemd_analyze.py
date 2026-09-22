import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('systemd-analyze tests')
@pytest.mark.smoke
@pytest.mark.systemd_analyze
class TestSystemdAnalyze:
    '''systemd-analyze smoke test class'''

    @allure.title('systemd-analyze: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', ['systemd-analyze'])
    def test_systemd_analyze_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utility via which'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f"systemd-analyze failed ({utility} not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('systemd-analyze: check workability')
    def test_systemd_analyze_workability(self, ssh_client: SshClient):
        '''Test systemd-analyze basic workability'''
        with allure.step('Check system boot-up time statistics'):
            cmd = ssh_client.exec('systemd-analyze time', ignore_rc=True)
            assert cmd.rc == 0, f"systemd-analyze failed (time command failed) out='{cmd.stdout}', err='{cmd.stderr}'"
