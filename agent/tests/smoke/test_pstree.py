import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('pstree tests')
@pytest.mark.smoke
@pytest.mark.pstree
class TestPstree:
    '''pstree smoke test class'''

    @allure.title('pstree: binary exists')
    @pytest.mark.minimal
    def test_pstree_binary_exists(self, ssh_client: SshClient):
        '''Test pstree binary installed'''
        with allure.step('Checking pstree binary'):
            cmd = ssh_client.exec('which pstree', ignore_rc=True)
            assert cmd.rc == 0, f"pstree failed (binary not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('pstree: process tree test')
    def test_pstree_functional(self, ssh_client: SshClient):
        '''Test pstree can display process tree'''
        with allure.step('Running pstree to show process tree'):
            cmd = ssh_client.exec('pstree', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pstree failed to show process tree: out='{cmd.stdout}', err='{cmd.stderr}'")
            # There must be at least one process
            check.is_true(len(cmd.stdout.strip(
            )) > 0, f"pstree output is empty: out='{cmd.stdout}', err='{cmd.stderr}'")
            # And pstree as well
            check.is_in('pstree', cmd.stdout, f"pstree failed: out='{cmd.stdout}', err='{cmd.stderr}'")
