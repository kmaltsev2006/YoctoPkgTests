import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('mc-helpers tests')
@pytest.mark.smoke
@pytest.mark.mc_helpers
class TestMcHelpers:
    '''
    Tests for mc-helpers package.
    Verifies existence of helper scripts and data files.
    '''

    @allure.title('mc-helpers: check directories existence')
    @pytest.mark.minimal
    def test_mc_helpers_dirs(self, ssh_client: SshClient):
        '''
        Minimal test: checks if standard mc directories exist.
        '''
        cmd = ssh_client.exec(
            'test -d /usr/libexec/mc || test -d /usr/lib/mc || test -d /usr/share/mc', ignore_rc=True)
        assert cmd.rc == 0, f"Mc-helpers failed (No MC helper directories found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('mc-helpers: scripts availability check')
    def test_mc_helpers_availability(self, ssh_client: SshClient):
        '''
        Verifies that helper scripts/binaries exist and are executable.
        Checks for cons.saver and extfs.d scripts without execution.
        '''
        helper_bin = 'cons.saver'

        with allure.step(f'Search for {helper_bin}'):
            find_cmd = ssh_client.exec(
                f'find /usr -name {helper_bin} -type f 2>/dev/null | head -n 1', ignore_rc=True)

        if find_cmd.rc == 0 and find_cmd.stdout.strip():
            path = find_cmd.stdout.strip()
            with allure.step(f'Check if {path} is executable'):
                cmd = ssh_client.exec(f'test -x {path}', ignore_rc=True)
                assert cmd.rc == 0, f"Mc-helpers failed (Helper {path} is not executable): out='{cmd.stdout}', err='{cmd.stderr}'"
        else:
            with allure.step('Check for extfs helpers directory'):
                cmd = ssh_client.exec(
                    'test -d /usr/libexec/mc/extfs.d/ || test -d /usr/lib/mc/extfs.d/', ignore_rc=True)
                check.equal(cmd.rc, 0, f"Mc-helpers failed (No extfs helpers found): out='{cmd.stdout}', err='{cmd.stderr}'")
