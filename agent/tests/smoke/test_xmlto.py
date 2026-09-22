import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('xmlto tests')
@pytest.mark.smoke
@pytest.mark.xmlto
class TestXmlto:
    '''xmlto smoke test class'''

    @allure.title('xmlto: check installation')
    @pytest.mark.minimal
    def test_xmlto_installation(self, ssh_client: SshClient):
        '''Check installed utilities'''        
        with allure.step('Check xmlto installation'):
            cmd = ssh_client.exec('which xmlto', ignore_rc=True)
            assert cmd.rc == 0, f"xmlto failed (xmlto not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('xmlto: check workability')
    @pytest.mark.parametrize('are_utils_available', [['fop']], indirect=True)
    def test_xmlto_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Test xmlto basic transformation to html'''
        ssh_client.put_file(f'{test_files_path}/test_xmlto.xml', remote_tmp_path)

        with allure.step('Convert XML to html and verify content'):
            cmd = ssh_client.exec(f'xmlto html {remote_tmp_path}/test_xmlto.xml --skip-validation --with-fop', ignore_rc=True)
            assert cmd.rc == 0, f"xmlto failed (transformation or content check failed) out='{cmd.stdout}', err='{cmd.stderr}'"
