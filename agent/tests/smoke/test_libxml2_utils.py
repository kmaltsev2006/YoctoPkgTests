import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('libxml2-utils tests')
@pytest.mark.smoke
@pytest.mark.libxml2_utils
class TestLibxml2Utils:
    '''libxml2-utils smoke test class'''

    @allure.title('libxml2-utils: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'xmllint',
        'xmlcatalog',
    ])
    def test_libxml2_utils_installation(self, ssh_client: SshClient, utility: str):
        '''Testing libxml2 utilities installed'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'{utility} is not installed: {cmd.stderr}')

    @allure.title('xmllint: check workability')
    @pytest.mark.minimal
    def test_libxml2_utils_xmllint_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing xmllint basic workability'''

        ssh_client.put_file(
            f'{test_files_path}/test_libxml2.xml', remote_tmp_path)

        with allure.step('Check xmllint workability'):
            cmd = ssh_client.exec(f'xmllint {remote_tmp_path}/test_libxml2.xml', ignore_rc=True)
            check.equal(cmd.rc, 0, f'xmllint failed: {cmd.stderr}')
            check.is_in('valid_xml_content', cmd.stdout, f'Unexpected output: {cmd.stdout}')

    @allure.title('xmlcatalog: check workability')
    @pytest.mark.minimal
    def test_libxml2_utils_xmlcatalog_workability(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Testing xmlcatalog basic workability'''
        catalog_file = f'{remote_tmp_path}/test_catalog.xml'

        with allure.step('Create and verify xml catalog'):
            cmd = ssh_client.exec(f'xmlcatalog --create --noout {catalog_file} && xmlcatalog {catalog_file}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'xmlcatalog failed: {cmd.stderr}')
