import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('go2xunit tests')
@pytest.mark.smoke
@pytest.mark.go2xunit
class TestGo2Xunit:
    '''go2xunit smoke tests'''

    @allure.title('go2xunit: binary runs and shows help')
    @pytest.mark.minimal
    def test_go2xunit_help(self, ssh_client: SshClient):
        '''Check that go2xunit binary exists and can be executed'''
        with allure.step('Running go2xunit with --help'):
            cmd = ssh_client.exec('go2xunit --help', ignore_rc=True)
            assert cmd.rc == 0, f'go2xunit failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('go2xunit: convert go test output file to junit xml')
    @pytest.mark.parametrize('are_utils_available', [['grep']], indirect=True)
    def test_go2xunit_convert_file(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Convert saved go test output to JUnit XML file'''
        with allure.step('Copy sample go test output to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_go2xunit_input.txt',
                f'{remote_tmp_path}/input.txt'
            )

        with allure.step('Run go2xunit and verify resulting xml contains <testsuite'):
            cmd = ssh_client.exec(
                f'go2xunit < {remote_tmp_path}/input.txt > {remote_tmp_path}/out.xml '
                f'&& grep -q "<testsuite" {remote_tmp_path}/out.xml',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'go2xunit failed (file convert): out="{cmd.stdout}", err="{cmd.stderr}"'
