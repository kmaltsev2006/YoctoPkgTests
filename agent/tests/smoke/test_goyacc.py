import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('goyacc tests')
@pytest.mark.smoke
@pytest.mark.goyacc
class TestGoyacc:
    '''goyacc smoke tests'''

    @allure.title('goyacc: binary runs and shows help')
    @pytest.mark.minimal
    def test_goyacc_help(self, ssh_client: SshClient):
        '''Check that goyacc binary exists and can be executed'''
        with allure.step('Running goyacc with -h'):
            cmd = ssh_client.exec('goyacc -h', ignore_rc=True)
            assert cmd.rc == 0, f'goyacc failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('goyacc: generate parser from minimal grammar')
    @pytest.mark.parametrize('are_utils_available', [['grep']], indirect=True)
    def test_goyacc_generate_parser(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Generate Go parser file from minimal .y grammar'''
        with allure.step('Copy minimal yacc grammar to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_goyacc_input.y',
                f'{remote_tmp_path}/input.y'
            )

        with allure.step('Run goyacc and verify generated Go file looks valid'):
            cmd = ssh_client.exec(
                f'goyacc -o {remote_tmp_path}/parser.go {remote_tmp_path}/input.y '
                f'&& grep -q "package" {remote_tmp_path}/parser.go',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'goyacc failed (generate): out="{cmd.stdout}", err="{cmd.stderr}"'
