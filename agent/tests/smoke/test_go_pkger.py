import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('go-pkger tests')
@pytest.mark.smoke
@pytest.mark.go_pkger
class TestGoPkger:
    '''go-pkger smoke tests'''

    @allure.title('go-pkger: binary runs and shows help')
    @pytest.mark.minimal
    def test_go_pkger_help(self, ssh_client: SshClient):
        '''Check that pkger binary exists and can be executed'''
        with allure.step('Running pkger with --help'):
            cmd = ssh_client.exec('pkger --help', ignore_rc=True)
            assert cmd.rc == 0, f'go-pkger failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('go-pkger: generate pkged.go for simple project')
    @pytest.mark.parametrize('are_utils_available', [['grep', 'mkdir', 'go']], indirect=True)
    def test_go_pkger_generate(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Run pkger on simple Go project and verify pkged.go is generated'''
        with allure.step('Prepare minimal Go project with assets'):
            cmd_prepare = ssh_client.exec(
                f'mkdir -p {remote_tmp_path}/assets '
                f'&& echo "package main; func main(){{}}" > {remote_tmp_path}/main.go '
                f'&& echo "hello" > {remote_tmp_path}/assets/test.txt '
                f'&& cd {remote_tmp_path} && go mod init testmodule',
                ignore_rc=True
            )
            check.equal(
                cmd_prepare.rc, 0, f'go-pkger failed (setup project): out="{cmd_prepare.stdout}", err="{cmd_prepare.stderr}"')

        with allure.step('Run pkger to generate embedded files'):
            cmd_pkger = ssh_client.exec(
                f'cd {remote_tmp_path} && pkger',
                ignore_rc=True
            )
            check.equal(
                cmd_pkger.rc, 0, f'go-pkger failed (pkger run): out="{cmd_pkger.stdout}", err="{cmd_pkger.stderr}"')

        with allure.step('Verify pkged.go file was created and looks valid'):
            cmd_check = ssh_client.exec(
                f'grep -q "package main" {remote_tmp_path}/pkged.go',
                ignore_rc=True
            )
            check.equal(
                cmd_check.rc, 0, f'go-pkger failed (check pkged.go): out="{cmd_check.stdout}", err="{cmd_check.stderr}"')
