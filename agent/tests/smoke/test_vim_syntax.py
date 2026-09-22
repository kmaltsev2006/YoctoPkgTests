import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('vim-syntax tests')
@pytest.mark.smoke
@pytest.mark.vim_syntax
class TestVimSyntax:
    '''vim-syntax smoke test class'''

    @allure.title('vim-syntax: check syntax directory')
    @pytest.mark.minimal
    def test_vim_syntax_directory(self, ssh_client: SshClient):
        '''Check existence of the syntax directory'''
        with allure.step('Check /usr/share/vim/syntax'):
            cmd = ssh_client.exec('find /usr/share/vim/*/syntax', ignore_rc=True)
            assert cmd.rc == 0, f"vim-syntax failed (syntax directory not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('vim-syntax: check workability')
    def test_vim_syntax_workability(self, ssh_client: SshClient):
        '''Test if syntax files are present and contain vim commands'''
        with allure.step('Verify any .vim file presence and content'):
            cmd = ssh_client.exec('grep -r -l "syn" /usr/share/vim/*/syntax | head -n 1 | xargs grep "syn"', ignore_rc=True)
            assert cmd.rc == 0, f"vim-syntax failed (no valid syntax scripts found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('vim-syntax: check file list')
    def test_vim_syntax_files_presence(self, ssh_client: SshClient):
        '''Check that the directory is not empty'''
        with allure.step('Check for multiple syntax files'):
            # Count files to ensure the package is not empty
            cmd = ssh_client.exec('ls /usr/share/vim/*/syntax/*.vim | wc -l', ignore_rc=True)
            assert cmd.rc == 0, f"vim-syntax failed (ls execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"
            # If the output is not '0', then files are present
            assert cmd.stdout.strip() != '0', f"vim-syntax failed (syntax directory is empty) out='{cmd.stdout}', err='{cmd.stderr}'"
