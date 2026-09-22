import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('ccache tests')
@pytest.mark.smoke
@pytest.mark.ccache
class TestCcache:
    '''ccache smoke test class'''

    @allure.title('ccache: check installation')
    @pytest.mark.minimal
    def test_ccache_version(self, ssh_client: SshClient):
        '''Testing ccache installed version'''
        with allure.step('Check ccache installation'):
            cmd = ssh_client.exec('which ccache', ignore_rc=True)
            assert cmd.rc == 0, f'ccache not installed: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('ccache: check -s option')
    @pytest.mark.minimal
    def test_ccache_s_option(self, ssh_client: SshClient):
        '''Testing ccache -s'''
        with allure.step('Check ccache -s option'):
            cmd = ssh_client.exec('ccache -s', ignore_rc=True)
            assert cmd.rc == 0, f'ccache failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('ccache: check -c option')
    @pytest.mark.minimal
    def test_ccache_c_option(self, ssh_client: SshClient):
        '''Testing ccache -c'''
        with allure.step('check ccache -c option'):
            cmd = ssh_client.exec('ccache -c', ignore_rc=True)
            assert cmd.rc == 0, f'ccache failed: out="{cmd.stdout}", err="{cmd.stderr}"'
