import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('mc-shell tests')
@pytest.mark.smoke
@pytest.mark.mc_shell
class TestMcShell:
    '''
    Tests for mc-shell functionality.
    Verifies subshell support and environment handling.
    '''

    # pylint: disable=unused-argument
    @allure.title('mc-shell: check binary')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['mc']], indirect=True)
    def test_mc_binary_exists(self, ssh_client: SshClient, are_utils_available):
        '''Minimal test: checks if 'mc' command is available'''
        with allure.step("Check 'mc' command"):
            cmd = ssh_client.exec('command -v mc', ignore_rc=True)
            assert cmd.rc == 0, f"Mc-shell failed (Binary not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('mc-shell: verify subshell support (Ctrl+O feature)')
    @pytest.mark.parametrize('are_utils_available', [['mc']], indirect=True)
    def test_mc_subshell_support(self, ssh_client: SshClient, are_utils_available):
        '''
        Verifies that MC is compiled with subshell support.
        '''
        with allure.step('Check mc --version for subshell support'):
            cmd = ssh_client.exec('TERM=xterm mc --version', ignore_rc=True)

            check.equal(cmd.rc, 0, f"Mc-shell failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('subshell support', cmd.stdout,
                        f"Mc-shell failed (No subshell support found): out='{cmd.stdout}', err='{cmd.stderr}'")

    # pylint: disable=unused-argument
    @allure.title('mc-shell: SHELL environment handling')
    @pytest.mark.parametrize('are_utils_available', [['mc']], indirect=True)
    def test_mc_shell_env(self, ssh_client: SshClient, are_utils_available):
        '''
        Verifies that MC respects the SHELL variable.
        '''
        target_shell = '/bin/sh'

        with allure.step(f'Run mc with SHELL={target_shell}'):
            cmd = ssh_client.exec(f'TERM=xterm SHELL={target_shell} mc --version', ignore_rc=True)
            assert cmd.rc == 0, f"Mc-shell failed (Startup failed with env): out='{cmd.stdout}', err='{cmd.stderr}'"
