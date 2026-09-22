import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('vim-vimrc tests')
@pytest.mark.smoke
@pytest.mark.vim_vimrc
class TestVimVimrc:
    '''vim-vimrc smoke test class'''

    @allure.title('vim-vimrc: check installation')
    @pytest.mark.minimal
    def test_vim_vimrc_installation(self, ssh_client: SshClient):
        '''Check if global vimrc file exists'''
        with allure.step('Check /etc/vim/vimrc presence'):
            cmd = ssh_client.exec('test -f /etc/vim/vimrc', ignore_rc=True)
            assert cmd.rc == 0, f"vim-vimrc failed (global config file not found) out='{cmd.stdout}', err='{cmd.stderr}'"
