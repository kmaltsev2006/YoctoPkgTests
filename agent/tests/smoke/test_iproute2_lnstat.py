import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-lnstat tests')
@pytest.mark.smoke
@pytest.mark.iproute2_lnstat
class TestIproute2Lnstat:
    '''iproute2-lnstat smoke test class'''

    @allure.title('iproute2-lnstat: version test')
    @pytest.mark.minimal
    def test_lnstat_version(self, ssh_client: SshClient):
        '''Test lnstat version'''
        with allure.step('Checking lnstat version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/lnstat -V', ignore_rc=True)
            # rc may be not 0, that is ok
            assert cmd.rc == 0 or 'version' in cmd.stdout.lower() or \
                'version' in cmd.stderr.lower(), f"iproute2-lnstat failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-lnstat: functional test')
    @pytest.mark.minimal
    def test_lnstat(self, ssh_client: SshClient):
        '''Test lnstat command functionality'''
        with allure.step('Checking lnstat command output'):
            cmd = ssh_client.exec('/sbin/lnstat -d 1 -c 1',
                                  ignore_rc=True)      # TODO: fix path
            # rc may be not 0, that is ok
            assert cmd.rc == 0 or '/proc/net/stat' in cmd.stdout.lower(
            ), f"lnstat -d 1 -c 1 failed: out='{cmd.stdout}', err='{cmd.stderr}'"
