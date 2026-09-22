import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-devlink tests')
@pytest.mark.smoke
@pytest.mark.iproute2_devlink
class TestIproute2Devlink:
    '''iproute2-devlink smoke test class'''

    @allure.title('iproute2-devlink: version test')
    @pytest.mark.minimal
    def test_devlink_version(self, ssh_client: SshClient):
        '''Test devlink version'''
        with allure.step('Checking devlink version'):
            cmd = ssh_client.exec('/sbin/devlink -V',
                                  ignore_rc=True)        # TODO: fix path
            assert cmd.rc == 0 and ('devlink utility' in cmd.stdout.lower(
            ) or 'iproute2' in cmd.stdout.lower()), f"iproute2-devlink failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-devlink: functional test')
    @pytest.mark.minimal
    def test_devlink(self, ssh_client: SshClient):
        '''Test devlink command functionality'''
        with allure.step('Checking devlink command output'):
            cmd = ssh_client.exec('/sbin/devlink dev list',
                                  ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0, f"devlink dev list failed: out='{cmd.stdout}', err='{cmd.stderr}'"
            # output may be just empty
