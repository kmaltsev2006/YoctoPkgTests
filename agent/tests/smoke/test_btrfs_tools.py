import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('btrfs-tools tests')
@pytest.mark.smoke
@pytest.mark.btrfs_tools
class TestBtrfsTools:
    '''btrfs-tools smoke test class'''

    @allure.title('btrfs-tools: check installation')
    @pytest.mark.minimal
    def test_btrfs_tools_version(self, ssh_client: SshClient):
        '''Testing btrfs installed'''
        with allure.step('Check btrfs-tools installation'):
            cmd = ssh_client.exec('which btrfs', ignore_rc=True)
            assert cmd.rc == 0, f'btrfs not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('btrfs-tools: check filesystem usage option')
    @pytest.mark.minimal
    def test_btrfs_tools_filesystem_usage(self, ssh_client: SshClient):
        '''Testing btrfs basic functionality'''
        with allure.step('Check btrfs-tools filesystem usage'):
            cmd = ssh_client.exec('btrfs filesystem usage /', ignore_rc=True)
            assert cmd.rc == 0 or cmd.stderr.startswith(
                'ERROR: not a btrfs filesystem'), f'btrfs is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
