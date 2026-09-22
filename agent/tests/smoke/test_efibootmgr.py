import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('efibootmgr tests')
@pytest.mark.smoke
@pytest.mark.efibootmgr
class TestBison:
    '''efibootmgr smoke test class'''

    @allure.title('efibootmgr: check installation')
    @pytest.mark.minimal
    def test_efibootmgr_installation(self, ssh_client: SshClient):
        '''Test efibootmgr installed'''
        with allure.step('Check efibootmgr installation'):
            cmd = ssh_client.exec('which efibootmgr', ignore_rc=True)
            assert cmd.rc == 0, f'efibootmgr not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('efibootmgr: check workability')
    @pytest.mark.minimal
    def test_efibootmgr_workability(self, ssh_client: SshClient):
        '''Test efibootmgr functionality'''
        with allure.step('efibootmgr: check workability'):
            cmd = ssh_client.exec_sudo('efibootmgr', ignore_rc=True)
            assert 'BootOrder:' in cmd.stdout or 'EFI variables are not supported on this system' in cmd.stderr, \
                f'efibootmgr is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
