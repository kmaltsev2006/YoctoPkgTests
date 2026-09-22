import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('lsb-release tests')
@pytest.mark.smoke
@pytest.mark.lsb_release
class TestLsbRelease:
    '''lsb-release smoke test class'''

    @allure.title('lsb-release: binary test')
    @pytest.mark.minimal
    def test_lsb_release_binary(self, ssh_client: SshClient):
        '''Test lsb_release command'''
        with allure.step('Checking lsb_release command'):
            cmd = ssh_client.exec('which lsb_release', ignore_rc=True)
            assert cmd.rc == 0, f'lsb_release not working: {cmd.stderr}'

    @allure.title('lsb-release: info test')
    def test_lsb_release_info(self, ssh_client: SshClient):
        '''Test lsb_release returns valid information'''
        with allure.step('Checking lsb_release output'):
            cmd = ssh_client.exec('lsb_release -a', ignore_rc=True)
            assert cmd.rc == 0 and 'Distributor ID' in cmd.stdout, f'lsb_release invalid output: {cmd.stderr}'
