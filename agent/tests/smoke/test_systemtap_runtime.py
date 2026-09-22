import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('systemtap-runtime tests')
@pytest.mark.smoke
@pytest.mark.systemtap_runtime
class TestSystemtapRuntime:
    '''systemtap-runtime smoke test class'''

    @allure.title('systemtap-runtime: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'staprun',
        'stapsh',
        'stap-merge'
    ])
    def test_systemtap_runtime_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities via which'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f"systemtap-runtime failed ({utility} not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('staprun: check workability')
    def test_systemtap_runtime_staprun_workability(self, ssh_client: SshClient):
        '''Test staprun basic workability'''
        with allure.step('Check staprun help output'):
            cmd = ssh_client.exec('staprun', ignore_rc=True)
            assert cmd.rc != 127, f"systemtap-runtime failed (staprun execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('stap-merge: check workability')
    def test_systemtap_runtime_merge_workability(self, ssh_client: SshClient):
        '''Test stap-merge basic workability'''
        with allure.step('Check stap-merge execution'):
            cmd = ssh_client.exec('stap-merge', ignore_rc=True)
            assert cmd.rc != 127, f"systemtap-runtime failed (stap-merge execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('systemtap-runtime: check helper scripts')
    @pytest.mark.minimal
    def test_systemtap_runtime_helpers(self, ssh_client: SshClient):
        '''Check existence of runtime helper directories'''
        with allure.step('Check systemtap runtime directory'):
            cmd = ssh_client.exec('test -d /usr/share/systemtap/runtime', ignore_rc=True)
            assert cmd.rc == 0, f"systemtap-runtime failed (runtime directory not found) out='{cmd.stdout}', err='{cmd.stderr}'"
