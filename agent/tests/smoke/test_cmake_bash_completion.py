import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cmake-bash-completion tests')
@pytest.mark.smoke
@pytest.mark.cmake_bash_completion
class TestCmakeBashCompletion:
    '''cmake-bash-completion smoke tests'''

    @allure.title('cmake-bash-completion: file exists')
    @pytest.mark.minimal
    def test_completion_file_exists(self, ssh_client: SshClient):
        '''Test cmake completion file exists on the target'''
        with allure.step('Verify that cmake completion file is present'):
            cmd = ssh_client.exec(
                'ls /usr/share/bash-completion/completions/cmake', 
                ignore_rc=True
                )
            assert cmd.rc == 0, 'cmake completion file missing in /usr/share/bash-completion/completions'

    # pylint: disable=unused-argument
    @allure.title('cmake-bash-completion: can be loaded manually')
    @pytest.mark.parametrize('are_utils_available', [['bash']], indirect=True)
    def test_completion_loads_manually(self, ssh_client: SshClient, are_utils_available: None):
        '''Test that bash-completion for cmake works when sourced manually'''
        with allure.step('Source completion file and verify that completion is registered'):
            cmd = ssh_client.exec(
                'bash -c "if [ -f /usr/share/bash-completion/completions/cmake ]; then '
                'source /usr/share/bash-completion/completions/cmake >/dev/null 2>&1 && complete -p cmake; '
                'else exit 2; fi"',
                ignore_rc=True
            )
            assert cmd.rc == 0, 'cmake completion file exists, but manual loading failed'
