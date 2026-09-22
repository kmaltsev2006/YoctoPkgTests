import pytest
import allure
from cyp_test_lib.ssh_client import SshClient, UnexpectedSshResponseException


@allure.suite('iproute2-tipc tests')
@pytest.mark.smoke
@pytest.mark.iproute2_tipc
class TestIproute2Tipc:
    '''iproute2-tipc smoke test class'''

    @allure.title('iproute2-tipc: version test')
    @pytest.mark.minimal
    def test_tipc_version(self, ssh_client: SshClient):
        '''Test tipc version'''
        with allure.step('Checking tipc version'):
            cmd = ssh_client.exec('/sbin/tipc --help',
                                  ignore_rc=True)        # TODO: fix path
            # package requires modprobe tipc
            assert cmd.rc == 0 or 'Transparent Inter-Process Communication Protocol' in cmd.stdout or \
                'Unable to get TIPC nl family id (module loaded?)' in cmd.stderr, f"iproute2-tipc failed (not installed):\
                      out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-tipc: functional test')
    @pytest.mark.minimal
    def test_tipc(self, ssh_client: SshClient):
        '''Test tipc command functionality'''
        with allure.step('Checking tipc command output'):
            cmd = ssh_client.exec('/sbin/tipc node list',
                                  ignore_rc=True)      # TODO: fix path
            # modprobe tipc required for this package to run
            assert 'node' in cmd.stdout.lower() or\
                'Unable to get TIPC nl family id (module loaded?)' in cmd.stderr, \
                f"tipc node list failed: out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-tipc: functional test (modprobe required)')
    def test_tipc_modprobe(self, ssh_client: SshClient):
        '''Test tipc command functionality with enabling with modprobe'''
        with allure.step('Enabling package with modprobe'):
            try:
                ssh_client.exec_sudo('/sbin/modprobe tipc')
            except UnexpectedSshResponseException:
                pytest.skip('modprobe unavaliable or cannot proceed')
        with allure.step('Checking tipc command output'):
            cmd = ssh_client.exec('/sbin/tipc node list',
                                  ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 and 'node' in cmd.stdout.lower(
            ), f"tipc node list failed: out='{cmd.stdout}', err='{cmd.stderr}'"
