import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient

@allure.suite('rdma-core tests')
@pytest.mark.smoke
@pytest.mark.rdma_core
class TestRdmaCore:
    '''rdma-core smoke test class'''

    @allure.title('rdma-core: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'ibv_devices',
        'ibv_devinfo',
        'rdma',
        'ibv_rc_pingpong',
        'ibv_ud_pingpong',
    ])
    def test_rdma_core_installation(self, ssh_client: SshClient, utility: str):
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'utility {utility} not found: {cmd.stderr}'

    @allure.title('rdma-core: check ibv_devices workability')
    @pytest.mark.minimal
    def test_rdma_core_ibv_devices(self, ssh_client: SshClient):
        with allure.step('Run ibv_devices'):
            cmd = ssh_client.exec('ibv_devices', ignore_rc=True)
            check.equal(cmd.rc, 0, f'ibv_devices failed: {cmd.stderr}')
            assert 'device' in cmd.stdout.lower() or 'node' in cmd.stdout.lower(), \
                f'Unexpected output: {cmd.stdout}'

    @allure.title('rdma-core: check rdma tool workability')
    @pytest.mark.minimal
    def test_rdma_core_tool_link(self, ssh_client: SshClient):
        with allure.step('Check rdma dev'):
            cmd = ssh_client.exec('rdma dev', ignore_rc=True)
            assert cmd.rc == 0, f'rdma tool failed: {cmd.stderr}'
