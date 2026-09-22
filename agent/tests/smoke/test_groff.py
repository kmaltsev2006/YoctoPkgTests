import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('groff tests')
@pytest.mark.smoke
@pytest.mark.groff
class TestGroff:
    '''Tests for the groff (GNU troff) document formatting system'''

    @allure.title('groff: minimal test')
    @pytest.mark.minimal
    def test_groff_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of grof'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('groff --version', ignore_rc=True)
            assert cmd.rc == 0, f"Groff failed (groff is not installed or not in PATH): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('groff: verify version and basic text formatting')
    def test_groff_functionality(self, ssh_client: SshClient) -> None:
        '''
        Verifies that groff is installed by checking its version.
        Performs a basic formatting test sending text via stdin and checking stdout.
        '''
        test_phrase = 'Hello Groff World'

        with allure.step('Verify basic formatting (pipeline echo -> groff)'):
            cmd = ssh_client.exec(
                f"echo '{test_phrase}' | groff -Tascii", ignore_rc=True)
            assert cmd.rc == 0 and test_phrase in cmd.stdout, f"Groff failed (formatting execution failed): out='{cmd.stdout}', err='{cmd.stderr}'"
