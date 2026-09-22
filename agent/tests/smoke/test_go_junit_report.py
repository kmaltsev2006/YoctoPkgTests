import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('go-junit-report tests')
@pytest.mark.smoke
@pytest.mark.go_junit_report
class TestGoJunitReport:
    '''go-junit-report smoke tests'''

    @allure.title('go-junit-report: binary runs and shows help')
    @pytest.mark.minimal
    def test_go_junit_report_help(self, ssh_client: SshClient):
        '''Check that go-junit-report binary exists and can be executed'''
        with allure.step('Running go-junit-report with --help'):
            cmd = ssh_client.exec('go-junit-report --help', ignore_rc=True)
            assert cmd.rc == 0, f'go-junit-report failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('go-junit-report: convert go test output to junit xml')
    @pytest.mark.parametrize('are_utils_available', [['grep']], indirect=True)
    def test_go_junit_report_convert(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Convert go test output to JUnit XML using go-junit-report'''
        with allure.step('Copy sample go test output to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_go_junit_report_input.txt',
                f'{remote_tmp_path}/input.txt'
            )

        with allure.step('Run go-junit-report and verify xml contains <testsuite'):
            cmd = ssh_client.exec(
                f'go-junit-report < {remote_tmp_path}/input.txt > {remote_tmp_path}/out.xml '
                f'&& grep -q "<testsuite" {remote_tmp_path}/out.xml',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'go-junit-report failed (convert): out="{cmd.stdout}", err="{cmd.stderr}"'
