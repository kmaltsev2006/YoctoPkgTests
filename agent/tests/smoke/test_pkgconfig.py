import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('pkgconfig tests')
@pytest.mark.smoke
@pytest.mark.pkgconfig
class TestPkgconfig:
    '''pkgconfig smoke test class'''

    @allure.title('pkgconfig: version test')
    @pytest.mark.minimal
    def test_pkgconfig_version(self, ssh_client: SshClient):
        '''Test pkgconfig version command'''
        with allure.step('Checking pkg-config version'):
            cmd = ssh_client.exec('pkg-config --version', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pkgconfig failed (version check): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('pkgconfig: list packages test')
    def test_pkgconfig_list_packages(self, ssh_client: SshClient):
        '''Test pkgconfig can list available packages'''
        with allure.step('Checking pkg-config list packages'):
            cmd = ssh_client.exec('pkg-config --list-all', ignore_rc=True)
            check.not_equal(cmd.rc, 127,
                            f"pkgconfig command not found: out='{cmd.stdout}', err='{cmd.stderr}'")
