import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-rtacct tests')
@pytest.mark.smoke
@pytest.mark.iproute2_rtacct
class TestIproute2Rtacct:
    '''iproute2-rtacct smoke test class'''

    @allure.title('iproute2-rtacct: version test')
    @pytest.mark.minimal
    def test_rtacct_version(self, ssh_client: SshClient):
        '''Test rtacct version'''
        with allure.step('Checking rtacct version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/rtacct -V', ignore_rc=True)
            assert cmd.rc == 0 and ('rtacct utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), f"iproute2-rtacct failed (not installed):\
                                          out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-rtacct: functional test')
    @pytest.mark.minimal
    def test_rtacct(self, ssh_client: SshClient):
        '''Test rtacct command functionality'''
        with allure.step('Checking rtacct command output'):
            cmd = ssh_client.exec(
                '/sbin/rtacct', ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'kernel' in cmd.stdout.lower(
            ), f"rtacct failed: out='{cmd.stdout}', err='{cmd.stderr}'"
