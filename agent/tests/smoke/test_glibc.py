import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('glibc tests')
@pytest.mark.smoke
@pytest.mark.glibc
class TestGlibc:
    '''glibc smoke tests'''

    @allure.title('glibc: minimal libc exists')
    @pytest.mark.minimal
    def test_glibc_libc_exists(self, ssh_client: SshClient):
        '''Check that libc.so exists in standard library paths'''
        with allure.step('Looking for libc.so in /usr/lib*'):
            cmd = ssh_client.exec('ls /usr/lib*/libc.so* 2>/dev/null | head -n1', ignore_rc=True)
            assert cmd.rc == 0, f'libc.so not found — glibc not installed: out="{cmd.stdout}", err="{cmd.stderr}"'
