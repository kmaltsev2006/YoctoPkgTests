import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('sed tests')
@pytest.mark.smoke
@pytest.mark.sed
class TestSed:
    '''sed smoke test class'''
    @allure.title('sed: stdout_test')
    def test_sed(self, ssh_client: SshClient):
        '''Tests basic functionality of sed'''
        command = "echo 'hello' | sed 's/hello/world/'"
        cmd = ssh_client.exec(command)
        assert 'world' in cmd.stdout, f"Sed failed: out='{cmd.stdout}', err='{cmd.stderr}'"
