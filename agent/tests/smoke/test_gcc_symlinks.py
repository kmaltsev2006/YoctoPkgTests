import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gcc-symlinks tests')
@pytest.mark.smoke
@pytest.mark.gcc_symlinks
class TestGccSymlinks:
    '''gcc-symlinks smoke tests'''

    @allure.title('gcc-symlinks: /usr/bin/gcc symlink exists')
    @pytest.mark.minimal
    def test_gcc_symlink_exists(self, ssh_client: SshClient):
        '''Check that /usr/bin/gcc symlink exists'''
        cmd = ssh_client.exec('test -L /usr/bin/gcc', ignore_rc=True)
        assert cmd.rc == 0, '/usr/bin/gcc symlink is missing'

    @allure.title('gcc-symlinks: /usr/bin/cc symlink exists')
    @pytest.mark.minimal
    def test_cc_symlink_exists(self, ssh_client: SshClient):
        '''Check that /usr/bin/cc symlink exists'''
        cmd = ssh_client.exec('test -L /usr/bin/cc', ignore_rc=True)
        assert cmd.rc == 0, '/usr/bin/cc symlink is missing'
