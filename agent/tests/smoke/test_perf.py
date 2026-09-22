import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('perf tests')
@pytest.mark.smoke
@pytest.mark.perf
class TestPerf:
    '''perf smoke test class'''
    @allure.title('perf: installed version test')
    @pytest.mark.minimal
    def test_perf_version(self, ssh_client: SshClient):
        '''Cheching perf installed version'''
        with allure.step('Cheching perf version'):
            cmd = ssh_client.exec('perf --version', ignore_rc=True)
            assert cmd.rc == 0, f"perf failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('perf: basic perf list test')
    @pytest.mark.minimal
    def test_perf_list(self, ssh_client: SshClient):
        '''Test basic perf list command'''
        with allure.step('Test basic perf listing'):
            cmd = ssh_client.exec('perf list', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"perf list failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            # Should have some events
            check.is_in('cpu', cmd.stdout.lower(),
                        f"perf list failed (expected 'cpu' in stdout): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('perf: perf stat test')
    @pytest.mark.minimal
    def test_perf_stat(self, ssh_client: SshClient):
        '''Test basic perf stat command'''
        with allure.step('Test basic perf listing'):
            cmd = ssh_client.exec('perf stat ls', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"perf stat ls failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            performance_indicators = ['cycles', 'branches', 'time elapsed']
            for indicator in performance_indicators:
                # responce can be in stderr for some reason
                check.is_true(indicator in cmd.stdout.lower(
                ) or indicator in cmd.stderr.lower(), f"perf failed (expected '{indicator}'): out='{cmd.stdout}', err='{cmd.stderr}'")
