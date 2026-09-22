import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('krb5 tests')
@pytest.mark.smoke
@pytest.mark.krb5
class TestKrb5:
    '''krb5 smoke test class'''

    @allure.title('krb5: binaries exist')
    @pytest.mark.minimal
    @pytest.mark.parametrize('binary', [
        '/usr/bin/kinit',
        '/usr/bin/klist',
        '/usr/bin/ktutil'
    ])
    def test_krb5_binaries_exist(self, binary, ssh_client: SshClient):
        '''Test krb5 binaries installed'''
        with allure.step(f'Checking {binary}'):
            cmd = ssh_client.exec(f'stat {binary}', ignore_rc=True)
            assert cmd.rc == 0, f"krb5 failed (binary not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('krb5: klist version test')
    @pytest.mark.minimal
    def test_klist_version(self, ssh_client: SshClient):
        '''Test klist version command'''
        with allure.step('Checking klist version'):
            cmd = ssh_client.exec('klist -V', ignore_rc=True)
            if cmd.rc != 0:
                cmd = ssh_client.exec('klist --version', ignore_rc=True)
            assert cmd.rc == 0, f"klist failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('krb5: klist functional test')
    @pytest.mark.minimal
    def test_klist_functional(self, ssh_client: SshClient):
        '''Test klist command functionality'''
        with allure.step('Checking klist output'):
            cmd = ssh_client.exec('klist', ignore_rc=True)
            # klist may return 1 if no credentials, but should output something
            assert cmd.rc == 0 or 'klist' in cmd.stdout.lower() or 'credential' in cmd.stdout.lower() \
                or 'cache' in cmd.stdout.lower() or 'ticket' in cmd.stdout.lower(), \
                f"klist failed: out='{cmd.stdout}', err='{cmd.stderr}'"
