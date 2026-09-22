import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('bison tests')
@pytest.mark.smoke
@pytest.mark.bison
class TestBison:
    '''bison smoke test class'''
    @allure.title('bison: check installation')
    @pytest.mark.minimal
    def test_bison_installation(self, ssh_client: SshClient):
        '''Testing bison installed'''
        with allure.step('Check bison installation'):
            cmd = ssh_client.exec('which bison', ignore_rc=True)
            assert cmd.rc == 0, f'Bison is not installed: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('bison: check workability')
    @pytest.mark.minimal
    def test_bison_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing bison basic functionality'''
        ssh_client.put_file(f'{test_files_path}/test_bison.y', remote_tmp_path)
        with allure.step('Compile'):
            cmd = ssh_client.exec(f'bison {remote_tmp_path}/test_bison.y -o {remote_tmp_path}/test_bison.tab.c && \
                                  cat {remote_tmp_path}/test_bison.tab.c', ignore_rc=True)
            assert cmd.rc == 0 and '#define YYBISON_VERSION' in cmd.stdout, f'bison is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
