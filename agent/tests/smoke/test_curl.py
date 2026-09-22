import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('curl tests')
@pytest.mark.smoke
@pytest.mark.curl
class TestCurl:
    '''curl smoke tests'''

    @allure.title('curl: installed and basic version check')
    @pytest.mark.minimal
    def test_curl_installed(self, ssh_client: SshClient):
        '''Check that curl is installed and reports version'''
        with allure.step('Checking that curl is installed'):
            cmd = ssh_client.exec('curl --version', ignore_rc=True)
            assert cmd.rc == 0, f'curl not installed: {cmd.stderr}'

    @allure.title('curl: fetch local file')
    def test_curl_fetch_local_file(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Check curl can fetch a local file correctly'''
        tmp_file = f'{remote_tmp_path}/test_curl_example.txt'
        content = 'Example Domain'

        with allure.step(f'Creating temporary file {tmp_file}'):
            ssh_client.exec(f"echo '{content}' > {tmp_file}")

        with allure.step(f'Fetching {tmp_file} using curl'):
            cmd = ssh_client.exec(f'curl -s file://{tmp_file}', ignore_rc=True)
            assert cmd.rc == 0 and content in cmd.stdout, f'curl failed: out = {cmd.stdout}, err = {cmd.stderr}'
