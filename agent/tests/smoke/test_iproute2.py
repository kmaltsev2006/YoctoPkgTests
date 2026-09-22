import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2 tests')
@pytest.mark.smoke
@pytest.mark.iproute2
class TestIproute2:
    '''iproute2 smoke test class'''

    @allure.title('iproute2: ip command version test')
    @pytest.mark.minimal
    def test_ip_command_version(self, ssh_client: SshClient):
        '''Test ip command version'''
        with allure.step('Checking ip command version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/ip -V', ignore_rc=True)
            assert cmd.rc == 0 and ('ip utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), \
                                        f"iproute2 failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2: ip command functional test')
    @pytest.mark.minimal
    def test_ip_command(self, ssh_client: SshClient):
        '''Test ip command functionality'''
        with allure.step('Checking ip addr output'):
            cmd = ssh_client.exec('/sbin/ip addr', ignore_rc=True)
            assert cmd.rc == 0 and 'loopback' in cmd.stdout.lower(
            ), f"ip addr failed: out='{cmd.stdout}', err='{cmd.stderr}'"
