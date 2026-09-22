import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gpp-symlinks tests')
@pytest.mark.smoke
@pytest.mark.gpp_symlinks
class TestGppSymlinks:
    '''g++-symlinks smoke tests'''

    @allure.title('g++-symlinks: /usr/bin/g++ symlink exists')
    @pytest.mark.minimal
    def test_gpp_symlink_exists(self, ssh_client: SshClient):
        '''Check that /usr/bin/g++ symlink exists'''
        cmd = ssh_client.exec('test -L /usr/bin/g++', ignore_rc=True)
        assert cmd.rc == 0, 'g++ symlink is missing'

    @allure.title('g++-symlinks: /usr/bin/c++ symlink exists')
    @pytest.mark.minimal
    def test_cxx_symlink_exists(self, ssh_client: SshClient):
        '''Check that /usr/bin/c++ symlink exists'''
        cmd = ssh_client.exec('test -L /usr/bin/c++', ignore_rc=True)
        assert cmd.rc == 0, 'c++ symlink is missing'
