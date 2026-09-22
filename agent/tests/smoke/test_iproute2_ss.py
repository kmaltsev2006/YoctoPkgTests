import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-ss tests')
@pytest.mark.smoke
@pytest.mark.iproute2_ss
class TestIproute2Ss:
    '''iproute2-ss smoke test class'''

    @allure.title('iproute2-ss: version test')
    @pytest.mark.minimal
    def test_ss_version(self, ssh_client: SshClient):
        '''Test ss version'''
        with allure.step('Checking ss version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/ss -V', ignore_rc=True)
            assert cmd.rc == 0 and ('ss utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), f"iproute2-ss failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-ss: functional test')
    @pytest.mark.minimal
    def test_ss(self, ssh_client: SshClient):
        '''Test ss command functionality'''
        with allure.step('Checking ss command output'):
            cmd = ssh_client.exec(
                '/sbin/ss', ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'netid' in cmd.stdout.lower(
            ), f"ss failed: out='{cmd.stdout}', err='{cmd.stderr}'"
