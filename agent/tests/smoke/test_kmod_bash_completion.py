import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('kmod-bash-completion tests')
@pytest.mark.smoke
@pytest.mark.kmod_bash_completion
class TestKmodBashCompletion:
    '''kmod-bash-completion smoke test class'''

    @allure.title('kmod-bash-completion: completion files exist')
    @pytest.mark.minimal
    def test_kmod_bash_completion_files(self, ssh_client: SshClient):
        '''Test kmod-bash-completion files installed'''
        with allure.step('Checking bash completion files'):
            cmd = ssh_client.exec(
                'stat /usr/share/bash-completion/completions/kmod',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"kmod-bash-completion failed (completion not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('kmod-bash-completion: source and test functionality')
    @pytest.mark.minimal
    def test_kmod_completion_functionality(self, ssh_client: SshClient):
        '''Test kmod completion can be sourced and works'''
        with allure.step('Testing completion functionality'):
            # Source completion and test tab completion
            test_script = '''
source /usr/share/bash-completion/completions/kmod 2>/dev/null
if type _kmod >/dev/null 2>&1; then
    echo "COMPLETION_FUNCTIONS_EXIST"
else
    echo "COMPLETION_FUNCTIONS_MISSING"
    exit 1
fi

# Check if completion works for kmod commands
if complete -p kmod 2>/dev/null | grep -q kmod; then
    echo "COMPLETION_WORKS_FOR_KMOD"
fi
'''
            cmd = ssh_client.exec(f'bash -c \'{test_script}\'', ignore_rc=True)
            assert 'COMPLETION_FUNCTIONS_EXIST' in cmd.stdout and 'COMPLETION_WORKS_FOR_KMOD' in cmd.stdout, \
                f"kmod-bash-completion failed: out='{cmd.stdout}', err='{cmd.stderr}'"
