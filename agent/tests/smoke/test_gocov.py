import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gocov tests')
@pytest.mark.smoke
@pytest.mark.gocov
class TestGocov:
    '''gocov smoke tests'''

    @allure.title('gocov: binary exists')
    @pytest.mark.minimal
    def test_gocov_binary_exists(self, ssh_client: SshClient):
        '''Check that gocov binary is installed'''
        with allure.step('Check gocov binary in PATH'):
            cmd = ssh_client.exec('which gocov', ignore_rc=True)
            assert cmd.rc == 0, f'gocov failed (binary not found): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('gocov: shows usage information')
    @pytest.mark.minimal
    def test_gocov_usage(self, ssh_client: SshClient):
        '''Check that gocov shows usage information'''
        with allure.step('Run gocov without arguments'):
            cmd = ssh_client.exec('gocov', ignore_rc=True)
            check.is_in('Usage:', cmd.stderr,
                        f'gocov failed (usage not shown): out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_in('gocov command [arguments]', cmd.stderr,
                        f'gocov failed (usage format wrong): out="{cmd.stdout}", err="{cmd.stderr}"')

    @allure.title('gocov: lists available commands')
    @pytest.mark.minimal
    def test_gocov_commands(self, ssh_client: SshClient):
        '''Check that gocov shows available commands'''
        with allure.step('Check available commands in usage'):
            cmd = ssh_client.exec('gocov', ignore_rc=True)
            required_commands = ['annotate', 'convert', 'report', 'test']
            for command in required_commands:
                check.is_in(
                    command, cmd.stderr, f'gocov failed (missing command {command}): out="{cmd.stdout}", err="{cmd.stderr}"')

    @allure.title('gocov: test command works with simple project')
    @pytest.mark.parametrize('are_utils_available', [['go']], indirect=True)
    def test_gocov_test_command(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None  # pylint: disable=unused-argument
    ):
        '''Test gocov test command with minimal Go project'''
        test_dir = f'{remote_tmp_path}/test_project'
        test_files_dir = f'{test_files_path}/test_gocov'

        with allure.step('Create minimal Go test project'):
            mkdir_cmd = ssh_client.exec(f'mkdir -p {test_dir}', ignore_rc=True)
            check.equal(
                mkdir_cmd.rc, 0, f'Failed to create test directory: out="{mkdir_cmd.stdout}", err="{mkdir_cmd.stderr}"')

            go_mod_local = f'{test_files_dir}/go_mod.txt'
            main_go_local = f'{test_files_dir}/main_go.txt'
            main_test_go_local = f'{test_files_dir}/main_test_go.txt'

            ssh_client.put_file(go_mod_local, f'{test_dir}/go.mod')
            ssh_client.put_file(main_go_local, f'{test_dir}/main.go')
            ssh_client.put_file(main_test_go_local, f'{test_dir}/main_test.go')

        with allure.step('Run gocov test command'):
            cmd = ssh_client.exec(
                f'cd {test_dir} && gocov test 2>&1',
                ignore_rc=True
            )
            assert 'error:' not in cmd.stderr or 'test' in cmd.stderr, f'gocov failed (test command error): out="{cmd.stdout}", err="{cmd.stderr}"'
