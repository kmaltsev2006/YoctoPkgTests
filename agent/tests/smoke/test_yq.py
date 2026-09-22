import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('yq tests')
@pytest.mark.smoke
@pytest.mark.yq
class TestYq:
    '''yq smoke test class'''

    # pylint: disable=unused-argument
    @allure.title('yq: stdout_test')
    @pytest.mark.parametrize('are_utils_available', [['yq']], indirect=True)
    def test_yq(self, ssh_client: SshClient, are_utils_available: None):
        '''Tests basic functionality of yq.'''
        command = "echo 'a: hello' | yq '.a'"
        cmd = ssh_client.exec(command, ignore_rc=True)
        assert cmd.rc == 0 and 'hello' in cmd.stdout, f"Yq failed: out='{cmd.stdout}', err='{cmd.stderr}'"
