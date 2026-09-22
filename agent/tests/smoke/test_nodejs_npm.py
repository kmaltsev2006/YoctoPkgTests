import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('nodejs-npm tests')
@pytest.mark.smoke
@pytest.mark.nodejs_npm
class TestNodejsNpm:
    '''nodejs-npm smoke test class'''

    @allure.title('nodejs-npm: check installation')
    @pytest.mark.minimal
    def test_nodejs_npm_installation(self, ssh_client: SshClient):
        with allure.step('Check nodejs-npm installation'):
            cmd = ssh_client.exec('which npm', ignore_rc=True)
            assert cmd.rc == 0, f'{cmd.stderr}'

    @allure.title('nodejs-npm: check workability')
    @pytest.mark.minimal
    def test_nodejs_npm_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test nodejs-npm command functionality'''
        with allure.step('Copy test_nodejs_npm.json to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_nodejs_npm.json', remote_tmp_path)
        with allure.step('Check npm workability with test file'):
            cmd = ssh_client.exec(f'cd {remote_tmp_path} && npm list', ignore_rc=True)
            assert cmd.rc == 0, f'npm is broken: {cmd.stderr}'
