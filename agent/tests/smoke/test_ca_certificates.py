import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('ca-certificates tests')
@pytest.mark.smoke
@pytest.mark.ca_certificates
class TestCaCertificates:
    '''ca-certificates smoke test class'''

    @allure.title('ca-certificates: check installation')
    @pytest.mark.minimal
    def test_ca_certificates_installation(self, ssh_client: SshClient):
        '''Testing ca-certificates basic functionality'''
        with allure.step('Check ca-certificates installation'):
            cmd = ssh_client.exec('test -f /etc/ssl/certs/ca-certificates.crt', ignore_rc=True)
            assert cmd.rc == 0, f'ca-certificates not found: out="{cmd.stdout}", err="{cmd.stderr}"'
