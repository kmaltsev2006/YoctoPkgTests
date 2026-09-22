import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-nstat tests')
@pytest.mark.smoke
@pytest.mark.iproute2_nstat
class TestIproute2Nstat:
    '''iproute2-nstat smoke test class'''

    @allure.title('iproute2-nstat: version test')
    @pytest.mark.minimal
    def test_nstat_version(self, ssh_client: SshClient):
        '''Test nstat version'''
        with allure.step('Checking nstat version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/nstat -V', ignore_rc=True)
            assert cmd.rc == 0 and ('nstat utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), f"iproute2-nstat failed (not installed):\
                                          out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-nstat: functional test')
    @pytest.mark.minimal
    def test_nstat(self, ssh_client: SshClient):
        '''Test nstat command functionality'''
        with allure.step('Checking nstat command output'):
            cmd = ssh_client.exec(
                '/sbin/nstat -a', ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'kernel' in cmd.stdout.lower(
            ), f"nstat -a failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"
