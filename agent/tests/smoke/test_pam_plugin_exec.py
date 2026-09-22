import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('pam-plugin-exec tests')
@pytest.mark.smoke
@pytest.mark.pam_plugin_exec
class TestPamPluginExec:
    '''pam-plugin-exec smoke tests'''

    @allure.title('pam-plugin-exec: module file exists')
    @pytest.mark.minimal
    def test_module_file_exists(self, ssh_client: SshClient):
        '''Test that PAM exec module exists'''
        with allure.step('Checking /lib/security/pam_exec.so'):
            cmd = ssh_client.exec(
                'ls /lib/security/pam_exec.so', ignore_rc=True)
            if cmd.rc != 0:
                cmd = ssh_client.exec(
                    'ls /usr/lib/security/pam_exec.so', ignore_rc=True)
            assert cmd.rc == 0, f'pam-plugin-exec failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('pam-plugin-exec: module is valid shared library')
    @pytest.mark.parametrize('are_utils_available', [['file', 'grep', 'strings']], indirect=True)
    def test_module_is_shared_object(
        self,
        ssh_client: SshClient,
        are_utils_available: None
    ):
        '''Verify that pam_exec.so is a valid shared object and exports PAM entry points'''

        with allure.step('Detect actual path to pam_exec.so'):
            cmd_path = ssh_client.exec(
                'if [ -f /lib/security/pam_exec.so ]; then '
                'echo /lib/security/pam_exec.so; '
                'elif [ -f /usr/lib/security/pam_exec.so ]; then '
                'echo /usr/lib/security/pam_exec.so; '
                'fi',
                ignore_rc=True
            )
            module_path = cmd_path.stdout.strip()
            check_path = module_path != ''

        with allure.step('Check file type is shared object'):
            cmd_file = ssh_client.exec(
                f'file "{module_path}" | grep -qi "shared object"',
                ignore_rc=True
            )

        with allure.step('Check module exports pam_sm_authenticate symbol'):
            cmd_symbols = ssh_client.exec(
                f'strings "{module_path}" | grep -q "pam_sm_authenticate"',
                ignore_rc=True
            )

        ok = (
            check_path and
            cmd_file.rc == 0 and
            cmd_symbols.rc == 0
        )

        assert ok, (
            f'pam-plugin-exec invalid module: '
            f'path="{module_path}", '
            f'file_err="{cmd_file.stderr}", '
            f'symbols_err="{cmd_symbols.stderr}"'
        )
