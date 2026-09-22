import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('e2fsprogs tests')
@pytest.mark.smoke
@pytest.mark.e2fsprogs
class TestE2fsprogs:
    '''e2fsprogs smoke test class'''

    @allure.title('e2fsprogs: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'badblocks',
        'chattr',
        'debugfs',
        'dumpe2fs',
        'e2fsck',
        'e2image',
        'e2label',
        'lsattr',
        'mke2fs',
        'mklost+found',
        'resize2fs',
        'tune2fs',
    ])
    def test_e2fsprogs_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'utility not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('badblocks: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_badblocks_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test badblocks functionality'''
        with allure.step('Copy test_e2fsprogs to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_e2fsprogs', remote_tmp_path)
        with allure.step('Check badblocks workability'):
            cmd = ssh_client.exec(
                f'badblocks -v {remote_tmp_path}/test_e2fsprogs', ignore_rc=True)
            assert cmd.rc == 0, f'badblocks has failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('chattr: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_chattr(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test chattr functionality'''
        with allure.step('Create test_chattr_file'):
            ssh_client.exec(f'touch {remote_tmp_path}/test_chattr_file')
        with allure.step('Check chattr workability'):
            cmd = ssh_client.exec(
                f'chattr +s {remote_tmp_path}/test_chattr_file', ignore_rc=True)
            assert cmd.rc == 0, f'chattr is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('debugfs: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_debugfs(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test debugfs functionality'''
        with allure.step('Copy test_e2fsprogs to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_e2fsprogs', remote_tmp_path)
        with allure.step('Check debugfs workability'):
            cmd = ssh_client.exec(
                f"debugfs -R 'ls' {remote_tmp_path}/test_e2fsprogs", ignore_rc=True)
            assert cmd.rc == 0 and cmd.stdout.startswith(' 2  (12) .    2  (12) ..    11  (4072) lost+found'), \
                f'debugfs is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('dumpe2fs: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_dumpe2fs(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy test_e2fsprogs to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_e2fsprogs', remote_tmp_path)
        with allure.step('Check dumpe2fs workability'):
            cmd = ssh_client.exec(
                f'dumpe2fs {remote_tmp_path}/test_e2fsprogs', ignore_rc=True)
            assert cmd.rc == 0 and 'Filesystem magic number:' in cmd.stdout, f'dumpe2fs is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('e2fsck: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_e2fsck(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy test_e2fsprogs to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_e2fsprogs', remote_tmp_path)
        with allure.step('Check e2fsck workability'):
            cmd = ssh_client.exec_sudo(
                f'e2fsck -y {remote_tmp_path}/test_e2fsprogs', ignore_rc=True)
            assert cmd.rc == 0 and 'test_e2fsprogs: clean, 11/128 files, 18/256 blocks' in cmd.stdout, \
                f'e2fsck is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('e2image: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_e2image(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy test_e2fsprogs to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_e2fsprogs', remote_tmp_path)
        with allure.step('Check e2image workability'):
            cmd = ssh_client.exec(
                f'e2image -r {remote_tmp_path}/test_e2fsprogs {remote_tmp_path}/sda_test_image', ignore_rc=True)
            check.equal(cmd.rc, 0, f'e2image creation failed: out="{cmd.stdout}", err="{cmd.stderr}"')
            cmd = ssh_client.exec(
                f'diff {remote_tmp_path}/test_e2fsprogs {remote_tmp_path}/sda_test_image', ignore_rc=True)
            check.equal(cmd.rc, 0, f'diff check failed: out="{cmd.stdout}", err="{cmd.stderr}"')

    @allure.title('e2label: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_e2label(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy e2label to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_e2fsprogs', remote_tmp_path)
        with allure.step('Check e2label workability'):
            cmd = ssh_client.exec(
                f'e2label {remote_tmp_path}/test_e2fsprogs new-label', ignore_rc=True)
            check.equal(cmd.rc, 0, f'setting label failed: out="{cmd.stdout}", err="{cmd.stderr}"')
            cmd = ssh_client.exec(
                f'e2label {remote_tmp_path}/test_e2fsprogs', ignore_rc=True)
            check.equal(cmd.rc, 0, f'reading label failed: out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_true(cmd.stdout == 'new-label',
                          f'e2label is broken: out="{cmd.stdout}", err="{cmd.stderr}"')

    @allure.title('lsattr: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_lsattr(self, ssh_client: SshClient, remote_tmp_path: str):
        with allure.step('Create test_lsattr_file'):
            ssh_client.exec(f'touch {remote_tmp_path}/test_lsattr_file')
        with allure.step('Check lsattr workability'):
            cmd = ssh_client.exec(
                f'lsattr {remote_tmp_path}/test_lsattr_file', ignore_rc=True)
            assert cmd.stdout.startswith(
                '--------------e-------'), f'lsattr is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('mke2fs: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_mke2fs(self, ssh_client: SshClient, remote_tmp_path: str):
        with allure.step('Check mke2fs workability'):
            cmd = ssh_client.exec_sudo(
                f'mke2fs {remote_tmp_path}/test_e2fsprogs 1024', ignore_rc=True)
            assert cmd.rc == 0 and 'Creating filesystem' in cmd.stdout, f'mke2fs is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('mklost+found: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_mklost_plus_found(self, ssh_client: SshClient, remote_tmp_path: str):
        with allure.step('Check mklost+found workability'):
            cmd = ssh_client.exec(
                f'(cd  {remote_tmp_path}; mklost+found)', ignore_rc=True)
            check.equal(cmd.rc, 0, f'mklost+found creation failed: out="{cmd.stdout}", err="{cmd.stderr}"')
            cmd = ssh_client.exec(
                f'test -e {remote_tmp_path}/lost+found', ignore_rc=True)
            check.equal(cmd.rc, 0, f'mklost+found is broken: out="{cmd.stdout}", err="{cmd.stderr}"')

    @allure.title('resize2fs: check workability')
    @pytest.mark.minimal
    def test_e2fsprogs_resize2fs(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy test_e2fsprogs to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_e2fsprogs', remote_tmp_path)

        with allure.step('Check resize2fs workability'):
            cmd = ssh_client.exec_sudo(
                f'resize2fs {remote_tmp_path}/test_e2fsprogs 2048', ignore_rc=True)
            check.equal(cmd.rc, 0, f'resize2fs command failed: out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_in('is now 2048 (4k) blocks long', cmd.stdout,
                        f'resize2fs is broken: out="{cmd.stdout}", err="{cmd.stderr}"')
