import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-genl tests')
@pytest.mark.smoke
@pytest.mark.iproute2_genl
class TestIproute2Genl:
    '''iproute2-genl smoke test class'''

    @allure.title('iproute2-genl: version test')
    @pytest.mark.minimal
    def test_genl_version(self, ssh_client: SshClient):
        '''Test genl version'''
        with allure.step('Checking genl version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/genl -V', ignore_rc=True)
            assert cmd.rc == 0 and ('genl utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), f"iproute2-genl failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-genl: functional test')
    @pytest.mark.minimal
    def test_genl(self, ssh_client: SshClient):
        '''Test genl command functionality'''
        with allure.step('Checking genl command output'):
            cmd = ssh_client.exec('/sbin/genl ctrl list',
                                  ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'name' in cmd.stdout.lower(
            ), f"genl ctrl list failed: out='{cmd.stdout}', err='{cmd.stderr}'"
