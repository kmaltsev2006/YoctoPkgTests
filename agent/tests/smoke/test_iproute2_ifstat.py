import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-ifstat tests')
@pytest.mark.smoke
@pytest.mark.iproute2_ifstat
class TestIproute2Ifstat:
    '''iproute2-ifstat smoke test class'''

    @allure.title('iproute2-ifstat: version test')
    @pytest.mark.minimal
    def test_ifstat_version(self, ssh_client: SshClient):
        '''Test ifstat version'''
        with allure.step('Checking ifstat version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/ifstat -V', ignore_rc=True)
            assert cmd.rc == 0 and ('ifstat utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), f"iproute2-ifstat failed (not installed):\
                                          out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-ifstat: functional test')
    @pytest.mark.minimal
    def test_ifstat(self, ssh_client: SshClient):
        '''Test ifstat command functionality'''
        with allure.step('Checking ifstat command output'):
            cmd = ssh_client.exec('/sbin/ifstat -a 1 1',
                                  ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'interface' in cmd.stdout.lower(
            ), f"ifstat -a 1 1 failed: out='{cmd.stdout}', err='{cmd.stderr}'"
