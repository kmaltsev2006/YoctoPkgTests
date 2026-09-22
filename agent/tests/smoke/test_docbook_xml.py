import pytest
import allure
from typing import Iterator
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('docbook xml tests')
@pytest.mark.smoke
@pytest.mark.docbook_xml
class TestDocbookXmlDtd:
    '''Tests for the docbook-xml-dtd4 package'''

    @pytest.fixture(scope='function', autouse=True)
    def setup_docbook_env(self, ssh_client: SshClient) -> Iterator[str]:
        '''Checks for xmllint and prepares test files'''

        catalog_path = ''

        cmd = ssh_client.exec('test -f /etc/xml/catalog', ignore_rc=True)
        if cmd.rc == 0:
            catalog_path = '/etc/xml/catalog'
        else:
            cmd = ssh_client.exec(
                'test -f /etc/xml/docbook-xml.xml', ignore_rc=True)
            if cmd.rc == 0:
                catalog_path = '/etc/xml/docbook-xml.xml'

        if catalog_path == '':
            pytest.fail(
                'Could not find XML catalog in /etc/xml/catalog or /etc/xml/docbook-xml.xml')

        yield catalog_path

    @allure.title('docbook-xml-dtd4: minimal test')
    @pytest.mark.minimal
    def test_docbook_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of docbook tools (xmllint)'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('xmllint --version', ignore_rc=True)
            assert cmd.rc == 0, f"docbook-xml failed (xmllint is not installed) out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('docbook-xml-dtd4: Validate a correct document')
    @pytest.mark.parametrize('are_utils_available', [['xmllint']], indirect=True)
    def test_dtd_with_valid_file(self, ssh_client: SshClient, setup_docbook_env: Iterator[str],
                                 test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests that a structurally correct DocBook XML file passes validation
        using the system-provided DTD.
        '''

        catalog_path = setup_docbook_env

        ssh_client.put_file(
            f'{test_files_path}/test_docbook_xml/valid.xml', remote_tmp_path)

        with allure.step(f'Run xmllint validation using catalog {catalog_path}'):
            cmd = ssh_client.exec(
                f'XML_CATALOG_FILES={catalog_path} xmllint --valid --noout --nonet {remote_tmp_path}/valid.xml', ignore_rc=True)
            check.equal(cmd.rc, 0, f"docbook-xml failed (Validation failed) out='{cmd.stdout}', err='{cmd.stderr}")

    # pylint: disable=unused-argument
    @allure.title('docbook-xml-dtd4: Reject an incorrect document')
    @pytest.mark.parametrize('are_utils_available', [['xmllint']], indirect=True)
    def test_dtd_with_invalid_file(self, ssh_client: SshClient, setup_docbook_env: Iterator[str],
                                   test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests that a structurally incorrect DocBook XML file fails validation
        and produces the expected error.
        '''

        catalog_path = setup_docbook_env

        ssh_client.put_file(
            f'{test_files_path}/test_docbook_xml/invalid.xml', remote_tmp_path)

        with allure.step('Run xmllint validation on the incorrect file'):
            cmd = ssh_client.exec(
                f'XML_CATALOG_FILES={catalog_path} xmllint --valid --noout --nonet {remote_tmp_path}/invalid.xml', ignore_rc=True)
            check.is_true(
                cmd.rc != 0, 'Validation unexpectedly passed for an incorrect document')
            check.is_in('validity error', cmd.stderr,
                        f"docbook-xml failed (Stderr did not contain the expected error message) out='{cmd.stdout}', err='{cmd.stderr}")
