import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('tzdata-core tests')
@pytest.mark.smoke
@pytest.mark.tzdata_core
class TestTzdataCore:
    '''tzdata-core smoke test class'''

    @allure.title('tzdata-core: check installation')
    @pytest.mark.minimal
    def test_tzdata_core_installation(self, ssh_client: SshClient):
        '''Check existence of zoneinfo directory'''
        with allure.step('Check zoneinfo directory'):
            cmd = ssh_client.exec('test -d /usr/share/zoneinfo', ignore_rc=True)
            assert cmd.rc == 0, f"tzdata-core failed (zoneinfo directory not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('tzdata-core: check workability')
    @pytest.mark.minimal
    def test_tzdata_core_workability(self, ssh_client: SshClient):
        '''Test timezone application via TZ variable'''
        with allure.step('Check UTC timezone application'):
            cmd = ssh_client.exec('TZ=UTC date +%Z', ignore_rc=True)
            assert cmd.rc == 0, f"tzdata-core failed (date command failed) out='{cmd.stdout}', err='{cmd.stderr}'"
            assert 'UTC' in cmd.stdout, f"tzdata-core failed (UTC not recognized) out='{cmd.stdout}', err='{cmd.stderr}'"
