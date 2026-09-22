import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('netbase tests')
@pytest.mark.smoke
@pytest.mark.netbase
class TestNetbaseTools:
    '''ncrurses-tools smoke test class'''

    @allure.title('netbase: check files availability')
    @pytest.mark.minimal
    @pytest.mark.parametrize('file', [
        '/etc/ethertypes',
        '/etc/protocols',
        '/etc/rpc',
        '/etc/services',
    ])
    def test_netbase_installation(self, ssh_client: SshClient, file: str):
        '''Check installed utilities'''
        with allure.step(f'Check {file} installation'):
            cmd = ssh_client.exec(f'test -f {file}', ignore_rc=True)
            assert cmd.rc == 0, f'{file} not found: {cmd.stderr}'

    @allure.title('/etc/ethertypes: check validity')
    @pytest.mark.minimal
    def test_netbase_ethertypes(self, ssh_client: SshClient):
        '''Test /etc/ethertypes file validity'''
        with allure.step('Check /etc/ethertypes validity'):
            cmd = ssh_client.exec('cat /etc/ethertypes', ignore_rc=True)
            assert 'Ethernet' in cmd.stdout, f'/etc/ethertypes is not valid: {cmd.stderr}'

    @allure.title('/etc/protocols: check validity')
    @pytest.mark.minimal
    def test_netbase_protocols(self, ssh_client: SshClient):
        '''Test /etc/protocols file validity'''
        with allure.step('Check /etc/protocols validity'):
            cmd = ssh_client.exec('cat /etc/protocols', ignore_rc=True)
            assert 'Internet' in cmd.stdout, f'/etc/protocols is not valid: {cmd.stderr}'

    @allure.title('/etc/rpc: check validity')
    @pytest.mark.minimal
    def test_netbase_rpc(self, ssh_client: SshClient):
        '''Test /etc/rpc file validity'''
        with allure.step('Check /etc/rpc validity'):
            cmd = ssh_client.exec('cat /etc/rpc', ignore_rc=True)
            assert 'rpc' in cmd.stdout, f'/etc/rpc is not valid: {cmd.stderr}'

    @allure.title('/etc/services: check validity')
    @pytest.mark.minimal
    def test_netbase_services(self, ssh_client: SshClient):
        '''Test /etc/services file validity'''
        with allure.step('Check /etc/services validity'):
            cmd = ssh_client.exec('cat /etc/services', ignore_rc=True)
            assert 'Network services' in cmd.stdout, f'/etc/services is not valid: {cmd.stderr}'
