import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('nodejs tests')
@pytest.mark.smoke
@pytest.mark.nodejs
class TestNodejs:
    '''nodejs smoke test class'''

    @allure.title('nodejs: check installation')
    @pytest.mark.minimal
    def test_nodejs_installation(self, ssh_client: SshClient):
        with allure.step('Check nodejs installation'):
            cmd = ssh_client.exec('which node', ignore_rc=True)
            assert cmd.rc == 0, f'{cmd.stderr}'

    @allure.title('nodejs: check workability')
    @pytest.mark.minimal
    def test_nodejs_workability(self, ssh_client: SshClient):
        '''Test node command functionality'''
        with allure.step('Check node workability'):
            cmd = ssh_client.exec('node -e "console.log(\'test\')"', ignore_rc=True)
            assert cmd.rc == 0 and 'test' in cmd.stdout, f'node is broken: {cmd.stderr}'
