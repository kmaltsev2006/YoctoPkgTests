import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('nftables tests')
@pytest.mark.smoke
@pytest.mark.nftables
class TestNftables:
    '''nftables smoke test class'''

    @allure.title('nftables: check installation')
    @pytest.mark.minimal
    def test_nftables_installation(self, ssh_client: SshClient):
        with allure.step('Check nftables installation'):
            cmd = ssh_client.exec('which nft', ignore_rc=True)
            assert cmd.rc == 0, f'{cmd.stderr}'

    @allure.title('nftables: check workability')
    @pytest.mark.minimal
    def test_nftables_workability(self, ssh_client: SshClient):
        '''Test nft command functionality'''
        with allure.step('Check nft workability'):
            cmd = ssh_client.exec_sudo('nft list ruleset')
            assert cmd.rc == 0, f'nft is broken: {cmd.stderr}'
