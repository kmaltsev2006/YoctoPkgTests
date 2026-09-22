import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('jq tests')
@pytest.mark.smoke
@pytest.mark.jq
class TestJq:
    '''jq smoke test class'''

    @allure.title('jq: version test')
    @pytest.mark.minimal
    def test_jq_version(self, ssh_client: SshClient):
        '''Test jq version'''
        with allure.step('Checking jq version'):
            cmd = ssh_client.exec('jq --help', ignore_rc=True)
            assert cmd.rc == 0, f"jq failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('jq: functional test')
    @pytest.mark.minimal
    def test_jq(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test jq command functionality'''
        json = '''
        {
            "some_data": 123
        }
        '''
        ssh_client.exec(f"echo '{json}' > {remote_tmp_path}/file.json")
        with allure.step('Checking jq command output'):
            cmd = ssh_client.exec(
                f"jq '.some_data' {remote_tmp_path}/file.json", ignore_rc=True)
            assert cmd.rc == 0 and '123' == cmd.stdout.lower(
            ), f"jq failed: out='{cmd.stdout}', err='{cmd.stderr}'"
