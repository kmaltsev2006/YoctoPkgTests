import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('xfsprogs tests')
@pytest.mark.smoke
@pytest.mark.xfsprogs
class TestXfsprogs:
    '''xfsprogs smoke test class'''

    @allure.title('xfsprogs: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'mkfs.xfs',
        'xfs_repair',
        'xfs_db',
        'xfs_admin',
        'xfs_copy',
        'xfs_metadump'
    ])
    def test_xfsprogs_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f"xfsprogs failed ({utility} not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('mkfs.xfs: check workability')
    def test_xfsprogs_mkfs_workability(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test mkfs.xfs functionality using a sparse file'''
        with allure.step('Create xfs image'):
            cmd = ssh_client.exec(
                f'dd if=/dev/zero of={remote_tmp_path}/test_xfsprogs.img bs=1M count=0 seek=350 && '
                f'mkfs.xfs -f -d file=1,size=350m {remote_tmp_path}/test_xfsprogs.img',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"xfsprogs failed (mkfs.xfs failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('xfs_db: check workability')
    def test_xfsprogs_xfs_db_workability(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test xfs_db with a functional flag'''
        with allure.step('Check xfs_db info'):
            cmd = ssh_client.exec(
                f'dd if=/dev/zero of={remote_tmp_path}/test_db.img bs=1M count=0 seek=350 && '
                f'mkfs.xfs -f -d file=1,size=350m {remote_tmp_path}/test_db.img && '
                f'xfs_db -r -c "sb 0" -c "p magicnum" {remote_tmp_path}/test_db.img',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"xfsprogs failed (xfs_db execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('xfs_admin: check workability')
    def test_xfsprogs_xfs_admin_workability(self, ssh_client: SshClient):
        '''Test xfs_admin execution'''
        with allure.step('Check xfs_admin help-like run'):
            cmd = ssh_client.exec('xfs_admin -u /dev/null', ignore_rc=True)
            assert cmd.rc not in [127, 139], f"xfsprogs failed (xfs_admin is broken) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('xfs_repair: check workability')
    def test_xfsprogs_xfs_repair_workability(self, ssh_client: SshClient):
        '''Test xfs_repair execution'''
        with allure.step('Check xfs_repair run on null device'):
            cmd = ssh_client.exec('xfs_repair -n /dev/null', ignore_rc=True)
            assert cmd.rc not in [127, 139], f"xfsprogs failed (xfs_repair is broken) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('xfs_metadump: check workability')
    def test_xfsprogs_xfs_metadump_workability(self, ssh_client: SshClient):
        '''Test xfs_metadump execution'''
        with allure.step('Check xfs_metadump run on null device'):
            cmd = ssh_client.exec('xfs_metadump -n /dev/null /dev/null', ignore_rc=True)
            assert cmd.rc not in [127, 139], f"xfsprogs failed (xfs_metadump is broken) out='{cmd.stdout}', err='{cmd.stderr}'"
