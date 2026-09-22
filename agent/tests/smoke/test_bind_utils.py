import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('bind-utils tests')
@pytest.mark.smoke
@pytest.mark.bind_utils
class TestBindUtils:
    '''bind-utils smoke test class'''

    @allure.title('bind-utils: dig version test')
    @pytest.mark.minimal
    def test_dig_version(self, ssh_client: SshClient):
        '''Test dig command version'''
        with allure.step('Checking dig version'):
            cmd = ssh_client.exec('dig -v')
            assert cmd.rc == 0, f"bind-utils failed (dig is not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('bind-utils: dig command test')
    @pytest.mark.minimal
    def test_dig_command(self, ssh_client: SshClient):
        '''Test dig command from bind-utils'''
        with allure.step('Testing basic DNS query with dig'):
            cmd = ssh_client.exec('dig localhost', ignore_rc=True)
            assert cmd.rc == 0 or '<<>> localhost' in cmd.stdout or 'global options' in cmd.stdout, f"dig failed:\
                  out='{cmd.stdout}', err='{cmd.stderr}'"
