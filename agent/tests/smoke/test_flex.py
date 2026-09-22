import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('flex tests')
@pytest.mark.smoke
@pytest.mark.flex
class TestFlex:
    '''flex smoke test class'''

    @allure.title('flex: check installation')
    @pytest.mark.minimal
    def test_flex_installation(self, ssh_client: SshClient):
        with allure.step('Check flex installation'):
            cmd = ssh_client.exec('which flex', ignore_rc=True)
            assert cmd.rc == 0, f'flex not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('flex: check workability')
    @pytest.mark.minimal
    def test_flex_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy test_flex.l to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_flex.l', remote_tmp_path)

        with allure.step('Compile'):
            cmd = ssh_client.exec(
                f'flex -o {remote_tmp_path}/lex.yy.c {remote_tmp_path}/test_flex.l', ignore_rc=True)
            check.equal(cmd.rc, 0, f'flex compilation failed: out="{cmd.stdout}", err="{cmd.stderr}"')

            cmd = ssh_client.exec(f'cat {remote_tmp_path}/lex.yy.c', ignore_rc=True)
            check.is_in('#define YY_FLEX_MAJOR_VERSION',
                        cmd.stdout, f'flex is broken: out="{cmd.stdout}", err="{cmd.stderr}"')
