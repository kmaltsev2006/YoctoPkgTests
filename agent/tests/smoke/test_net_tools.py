import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('net-tools tests')
@pytest.mark.smoke
@pytest.mark.net_tools
class TestNetTools:
    '''net-tools smoke test class'''

    @allure.title('net-tools: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'arp',
        'dnsdomainname',
        'domainname',
        'hostname',
        'ifconfig',
        'nameif',
        'netstat',
        'nisdomainname',
        'plipconfig',
        'rarp',
        'route',
        'slattach',
        'ypdomainname',
    ])
    def test_net_tools_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'utility not found: {cmd.stderr}'

    @allure.title('arp: check workability')
    @pytest.mark.minimal
    def test_net_tools_arp(self, ssh_client: SshClient):
        '''Test arp command functionality'''
        with allure.step('Check arp workability'):
            cmd = ssh_client.exec('arp', ignore_rc=True)
            assert cmd.rc == 0, f'arp has failed: {cmd.stderr}'

    @allure.title('dnsdomainname: check workability')
    @pytest.mark.minimal
    def test_net_tools_dnsdomainname(self, ssh_client: SshClient):
        '''Test dnsdomainname command functionality'''
        with allure.step('Check dnsdomainname workability'):
            cmd = ssh_client.exec('dnsdomainname', ignore_rc=True)
            assert cmd.rc == 0, f'dnsdomainname has failed: {cmd.stderr}'

    @allure.title('domainname: check workability')
    @pytest.mark.minimal
    def test_net_tools_domainname(self, ssh_client: SshClient):
        '''Test domainname command functionality'''
        with allure.step('Check domainname workability'):
            cmd = ssh_client.exec('domainname', ignore_rc=True)
            assert cmd.rc == 0, f'domainname has failed: {cmd.stderr}'

    @allure.title('hostname: check workability')
    @pytest.mark.minimal
    def test_net_tools_hostname(self, ssh_client: SshClient):
        '''Test hostname command functionality'''
        with allure.step('Check hostname workability'):
            cmd = ssh_client.exec('hostname', ignore_rc=True)
            assert cmd.rc == 0, f'hostname has failed: {cmd.stderr}'

    @allure.title('ifconfig: check workability')
    @pytest.mark.minimal
    def test_net_tools_ifconfig(self, ssh_client: SshClient):
        '''Test ifconfig command functionality'''
        with allure.step('Check ifconfig workability'):
            cmd = ssh_client.exec('ifconfig -a', ignore_rc=True)
            assert cmd.rc == 0, f'ifconfig has failed: {cmd.stderr}'

    @allure.title('nameif: check workability')
    @pytest.mark.minimal
    def test_net_tools_nameif(self, ssh_client: SshClient):
        '''Test nameif command functionality'''
        with allure.step('Check nameif workability'):
            cmd = ssh_client.exec_sudo('nameif eth0 nameif-test', ignore_rc=True)
            assert cmd.rc in [0, 1, 2], f'nameif has failed: {cmd.stderr}'

    @allure.title('netstat: check workability')
    @pytest.mark.minimal
    def test_net_tools_netstat(self, ssh_client: SshClient):
        '''Test netstat command functionality'''
        with allure.step('Check netstat workability'):
            cmd = ssh_client.exec('netstat -r', ignore_rc=True)
            assert cmd.rc == 0, f'netstat has failed: {cmd.stderr}'

    @allure.title('nisdomainname: check workability')
    @pytest.mark.minimal
    def test_net_tools_nisdomainname(self, ssh_client: SshClient):
        '''Test nisdomainname command functionality'''
        with allure.step('Check nisdomainname workability'):
            cmd = ssh_client.exec('nisdomainname', ignore_rc=True)
            assert cmd.rc == 0, f'nisdomainname has failed: {cmd.stderr}'

    @allure.title('plipconfig: check workability')
    @pytest.mark.minimal
    def test_net_tools_plipconfig(self, ssh_client: SshClient):
        '''Test plipconfig command functionality'''
        with allure.step('Check plipconfig workability'):
            cmd = ssh_client.exec_sudo('plipconfig parport0', ignore_rc=True)
            assert cmd.rc == 0 or 'ioctl: No such device' in cmd.stderr, f'plipconfig has failed: {cmd.stderr}'

    @allure.title('rarp: check workability')
    @pytest.mark.minimal
    def test_net_tools_rarp(self, ssh_client: SshClient):
        '''Test rarp command functionality'''
        with allure.step('Check rarp workability'):
            cmd = ssh_client.exec('rarp -a', ignore_rc=True)
            assert cmd.rc == 0 or 'This kernel does not support RARP.' in cmd.stderr, f'rarp has failed: {cmd.stderr}'

    @allure.title('route: check workability')
    @pytest.mark.minimal
    def test_net_tools_route(self, ssh_client: SshClient):
        '''Test route command functionality'''
        with allure.step('Check route workability'):
            cmd = ssh_client.exec('route -n', ignore_rc=True)
            assert cmd.rc == 0, f'route has failed: {cmd.stderr}'

    @allure.title('slattach: check workability')
    @pytest.mark.minimal
    def test_net_tools_slattach(self, ssh_client: SshClient):
        '''Test slattach command functionality'''
        with allure.step('Check slattach workability'):
            cmd = ssh_client.exec_sudo('slattach /dev/null', ignore_rc=True)
            assert cmd.rc == 0 or 'Inappropriate ioctl for device' in cmd.stderr, f'slattach has failed: {cmd.stderr}'

    @allure.title('ypdomainname: check workability')
    @pytest.mark.minimal
    def test_net_tools_ypdomainname(self, ssh_client: SshClient):
        '''Test ypdomainname command functionality'''
        with allure.step('Check ypdomainname workability'):
            cmd = ssh_client.exec('ypdomainname', ignore_rc=True)
            assert cmd.rc == 0, f'ypdomainname has failed: {cmd.stderr}'
