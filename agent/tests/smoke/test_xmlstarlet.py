import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('xmlstarlet tests')
@pytest.mark.smoke
@pytest.mark.xmlstarlet
class TestXmlstarlet:
    '''xmlstarlet smoke test class'''

    @allure.title('xmlstarlet: check installation')
    @pytest.mark.minimal
    def test_xmlstarlet_installation(self, ssh_client: SshClient):
        '''Check xmlstarlet installation'''
        with allure.step('Check xmlstarlet installation'):
            cmd = ssh_client.exec('which xmlstarlet', ignore_rc=True)
            assert cmd.rc == 0, f"xmlstarlet failed (xmlstarlet not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('xmlstarlet: check workability')
    def test_xmlstarlet_workability(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test xmlstarlet basic selection functionality'''
        with allure.step('Create test XML and select data'):
            cmd = ssh_client.exec(
                f'echo "<data><status>xml_ok</status></data>" > {remote_tmp_path}/test_xmlstarlet.xml && '
                f'xmlstarlet sel -t -v "/data/status" {remote_tmp_path}/test_xmlstarlet.xml',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f"xmlstarlet failed (selection failed) out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('xml_ok', cmd.stdout, f"xmlstarlet failed (unexpected output) out='{cmd.stdout}', err='{cmd.stderr}'")
