import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-routel tests')
@pytest.mark.smoke
@pytest.mark.iproute2_routel
class TestIproute2Routel:
    '''iproute2-routel smoke test class'''

    @allure.title('iproute2-routel: version test')
    @pytest.mark.minimal
    def test_routel_version(self, ssh_client: SshClient):
        '''Test routel version'''
        with allure.step('Checking routel version'):
            cmd = ssh_client.exec('/sbin/routel --help',
                                  ignore_rc=True)        # TODO: fix path
            # rc may be not 0
            assert cmd.rc == 0 or 'usage' in cmd.stderr.lower() or 'usage' in cmd.stdout.lower(), f"iproute2-routel failed (not installed):\
                  out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-routel: functional test')
    @pytest.mark.minimal
    def test_routel(self, ssh_client: SshClient):
        '''Test routel command functionality'''
        with allure.step('Checking routel command output'):
            cmd = ssh_client.exec(
                '/sbin/routel', ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'gateway' in cmd.stdout.lower(
            ), f"routel failed: out='{cmd.stdout}', err='{cmd.stderr}'"
