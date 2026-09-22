import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('iproute2-rdma tests')
@pytest.mark.smoke
@pytest.mark.iproute2_rdma
class TestIproute2Rdma:
    '''iproute2-rdma smoke test class'''

    @allure.title('iproute2-rdma: version test')
    @pytest.mark.minimal
    def test_rdma_version(self, ssh_client: SshClient):
        '''Test rdma version'''
        with allure.step('Checking rdma version'):
            # TODO: fix path
            cmd = ssh_client.exec('/sbin/rdma -V', ignore_rc=True)
            assert cmd.rc == 0 and ('rdma utility' in cmd.stdout.lower() or
                                    'iproute2' in cmd.stdout.lower()), f"iproute2-rdma failed (not installed):\
                                          out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('iproute2-rdma: functional test')
    @pytest.mark.minimal
    def test_rdma(self, ssh_client: SshClient):
        '''Test rdma command functionality'''
        with allure.step('Checking rdma command output'):
            cmd = ssh_client.exec('/sbin/rdma dev show',
                                  ignore_rc=True)      # TODO: fix path
            assert cmd.rc == 0 or 'Failed to open NETLINK_RDMA socket' in cmd.stderr, f"rdma dev show failed: out='{cmd.stdout}', err='{cmd.stderr}'"
            # output may be empty
