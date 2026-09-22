import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('systemd-rpm-macros tests')
@pytest.mark.smoke
@pytest.mark.systemd_rpm_macros
class TestSystemdRpmMacros:
    '''systemd-rpm-macros smoke test class'''

    @allure.title('systemd-rpm-macros: check installation')
    @pytest.mark.minimal
    def test_systemd_rpm_macros_installation(self, ssh_client: SshClient):
        '''Check macros file exists'''
        with allure.step('Check macros.systemd file'):
            cmd = ssh_client.exec('test -f /usr/lib/rpm/macros.d/macros.systemd', ignore_rc=True)
            assert cmd.rc == 0, f"systemd-rpm-macros failed (macros.systemd file not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('systemd-rpm-macros: check macros expansion')
    @pytest.mark.minimal
    @pytest.mark.parametrize('macro', ['%{_unitdir}', '%{_tmpfilesdir}'])
    def test_systemd_macros_expansion(self, ssh_client: SshClient, macro: str):
        '''Test that systemd macros expand to paths'''
        with allure.step(f'Expand {macro}'):
            cmd = ssh_client.exec(f'rpm --eval "{macro}"', ignore_rc=True)
            check.equal(cmd.rc, 0, f"systemd-rpm-macros failed (failed to eval {macro}) out='{cmd.stdout}', err='{cmd.stderr}'")
            check.not_equal(cmd.stdout.strip(), macro, f"systemd-rpm-macros failed out='{cmd.stdout}', err='{cmd.stderr}'")

    # pylint: disable=unused-argument
    @allure.title('systemd-rpm-macros: check workability')
    @pytest.mark.parametrize('are_utils_available', [['rpmbuild']], indirect=True)
    def test_systemd_macros_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing macros workability via rpmbuild parse'''
        ssh_client.put_file(f'{test_files_path}/test_systemd_rpm_macros.spec', remote_tmp_path)

        with allure.step('Parse spec file to check macros expansion'):
            cmd = ssh_client.exec(f'rpmbuild --parse {remote_tmp_path}/test_systemd_rpm_macros.spec', ignore_rc=True)
            assert cmd.rc == 0, f"systemd-rpm-macros failed (spec file parsing failed) out='{cmd.stdout}', err='{cmd.stderr}'"
