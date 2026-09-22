import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('systemtap tests')
@pytest.mark.smoke
@pytest.mark.systemtap
class TestSystemtap:
    '''systemtap smoke test class'''

    @allure.title('systemtap: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', ['stap', 'staprun'])
    def test_systemtap_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities via which'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f"systemtap failed ({utility} not found) out='{cmd.stdout}', err='{cmd.stderr}'"
