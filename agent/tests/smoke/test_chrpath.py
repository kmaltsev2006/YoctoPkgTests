import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('chrpath tests')
@pytest.mark.smoke
@pytest.mark.chrpath
class TestChrpath:
    '''chrpath smoke test class'''

    @allure.title('chrpath: check installation')
    @pytest.mark.minimal
    def test_chrpath_version(self, ssh_client: SshClient):
        '''Testing chrpath installed'''
        with allure.step('Check chrpath installation'):
            cmd = ssh_client.exec('which chrpath', ignore_rc=True)
            assert cmd.rc == 0, f'chrpath not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('chrpath: check -l option')
    @pytest.mark.minimal
    def test_chrpath_l_option(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing chrpath -l'''
        ssh_client.put_file(
            f'{test_files_path}/test_chrpath', remote_tmp_path)

        with allure.step('Check chrpath -l option'):
            cmd = ssh_client.exec(
                f'chrpath -l {remote_tmp_path}/test_chrpath', ignore_rc=True)
            assert cmd.rc == 2 and cmd.stdout == f'{remote_tmp_path}/test_chrpath: no rpath or runpath tag found.', \
                f'chrpath is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
