import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('kmod tests')
@pytest.mark.smoke
@pytest.mark.kmod
class TestKmod:
    '''kmod smoke test class'''

    @allure.title('kmod: binaries exist')
    @pytest.mark.minimal
    @pytest.mark.parametrize('binary', [
        '/usr/bin/kmod',
        '/usr/bin/lsmod'
    ])
    def test_kmod_binaries_exist(self, binary, ssh_client: SshClient):
        '''Test kmod binaries installed'''
        with allure.step(f'Checking {binary}'):
            cmd = ssh_client.exec(f'stat {binary}', ignore_rc=True)
            assert cmd.rc == 0, f"kmod failed (binary not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('kmod: version test')
    @pytest.mark.minimal
    def test_kmod_version(self, ssh_client: SshClient):
        '''Test kmod version'''
        with allure.step('Checking kmod version'):
            cmd = ssh_client.exec('kmod --version', ignore_rc=True)
            assert cmd.rc == 0, f"kmod failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('kmod: lsmod functional test')
    @pytest.mark.minimal
    def test_lsmod_works(self, ssh_client: SshClient):
        '''Test lsmod functionality'''
        with allure.step('Running lsmod to list modules'):
            cmd = ssh_client.exec('lsmod', ignore_rc=True)
            assert cmd.rc == 0 and 'Module' in cmd.stdout, f"lsmod failed: out='{cmd.stdout}', err='{cmd.stderr}'"
