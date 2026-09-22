import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('vim-common tests')
@pytest.mark.smoke
@pytest.mark.vim_common
class TestVimCommon:
    '''vim-common smoke test class'''

    @allure.title('vim-common: check installation')
    @pytest.mark.minimal
    def test_vim_common_installation(self, ssh_client: SshClient):
        '''Check xxd installation'''
        with allure.step('Check xxd installation'):
            cmd = ssh_client.exec('which xxd', ignore_rc=True)
            assert cmd.rc == 0, f"vim-common failed (xxd not found) out='{cmd.stdout}', err='{cmd.stderr}'"


    @allure.title('vim-common: check support files')
    @pytest.mark.minimal
    def test_vim_common_support_files(self, ssh_client: SshClient):
        '''Check existence of main vim runtime directory'''
        with allure.step('Check /usr/share/vim directory'):
            cmd = ssh_client.exec('test -d /usr/share/vim', ignore_rc=True)
            assert cmd.rc == 0, f"vim-common failed (runtime directory not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('xxd: check workability')
    def test_vim_common_xxd_workability(self, ssh_client: SshClient):
        '''Test xxd utility functionality'''
        with allure.step('Check hex dump and reverse'):
            cmd = ssh_client.exec(
                'echo "vim_test" | xxd | xxd -r', 
                ignore_rc=True
            )
            assert cmd.rc == 0, f"vim-common failed (xxd transformation failed) out='{cmd.stdout}', err='{cmd.stderr}'"
            assert 'vim_test' in cmd.stdout, f"vim-common failed (unexpected xxd output) out='{cmd.stdout}', err='{cmd.stderr}'"
