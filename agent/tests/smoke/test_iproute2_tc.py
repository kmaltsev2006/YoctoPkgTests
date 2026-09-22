import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-tc tests')
@pytest.mark.smoke
@pytest.mark.iproute2_tc
class TestIproute2Tc:
    '''iproute2-tc smoke test class'''

    @allure.title('iproute2-tc: version test')
    @pytest.mark.minimal
    def test_tc_version(self, ssh_client: SshClient):
        '''Test tc version'''
        with allure.step('Checking tc version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/tc -V', ignore_rc=True)
            assert cmd.rc == 0 and ('tc utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), f"iproute2-tc failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-tc: functional test')
    @pytest.mark.minimal
    def test_tc(self, ssh_client: SshClient):
        '''Test tc command functionality'''
        with allure.step('Checking tc command output'):
            cmd = ssh_client.exec('/sbin/tc qdisc show',
                                  ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'refcnt' in cmd.stdout.lower(
            ), f"tc qdisc show failed: out='{cmd.stdout}', err='{cmd.stderr}'"
