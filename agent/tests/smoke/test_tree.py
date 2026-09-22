import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('tree tests')
@pytest.mark.smoke
@pytest.mark.tree
class TestTree:
    '''tree smoke test class'''
    @allure.title('tree: version test')
    @pytest.mark.minimal
    def test_tree_version(self, ssh_client: SshClient):
        '''Test installed tree version'''
        with allure.step('Checking installed version'):
            cmd = ssh_client.exec('tree --version', ignore_rc=True)
            assert cmd.rc == 0, f"tree failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('tree: basic functionality test')
    @pytest.mark.minimal
    def test_tree(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test basic tree command'''
        test_cmds = [
            f'mkdir -p {remote_tmp_path}/tree_test/dir1/dir2',
            f"echo 'test' > {remote_tmp_path}/tree_test/file1.txt",
            f"echo 'test' > {remote_tmp_path}/tree_test/dir1/file2.txt"
        ]
        with allure.step('Setting up test files'):
            for cmd_text in test_cmds:
                ssh_client.exec(cmd_text)
        with allure.step('Checking tree command output'):
            cmd = ssh_client.exec(
                f'tree {remote_tmp_path}/tree_test', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"tree failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            entries = ['dir1', 'file1.txt', 'file2.txt']
            for entry in entries:
                check.is_in(entry, cmd.stdout,
                            f"tree failed (expected '{entry}' in stdout): out='{cmd.stdout}', err='{cmd.stderr}'")
