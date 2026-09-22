import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('docbook xsl tests')
@pytest.mark.smoke
@pytest.mark.docbook_xsl
class TestDocbookXslStylesheets:
    '''Tests for the docbook-xsl-stylesheets package'''

    @allure.title('docbook-xsl-stylesheets: minimal test')
    @pytest.mark.minimal
    def test_docbook_xsl_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of docbook xsl tools (xsltproc)'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('xsltproc --version', ignore_rc=True)
            assert cmd.rc == 0, f"docbook-xsl failed (xsltproc is not installed) out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('docbook-xsl-stylesheets: Transform DocBook XML to HTML')
    @pytest.mark.parametrize('are_utils_available', [['xsltproc']], indirect=True)
    def test_xsl_transformation_to_html(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests that a DocBook XML file can be successfully transformed into an HTML file
        using the system-provided XSL stylesheets.
        '''

        ssh_client.put_file(
            f'{test_files_path}/test_docbook_xsl.xml', remote_tmp_path)

        with allure.step('Run xsltproc to transform XML to HTML'):
            xsl_stylesheet_path = '/usr/share/xml/docbook/xsl-stylesheets-1.79.1/xhtml/docbook.xsl'
            transform_command = f'xsltproc -o {remote_tmp_path}/output.html {xsl_stylesheet_path} {remote_tmp_path}/test_docbook_xsl.xml'

            cmd = ssh_client.exec(transform_command, ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"docbook-xsl failed (xsltproc in not installed) out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Verify the content of the generated HTML file'):
            check_html_cmd = ssh_client.exec(
                f'cat {remote_tmp_path}/output.html', ignore_rc=True)
            check.equal(check_html_cmd.rc, 0,
                        f"docbook-xsl failed (Failed to read the generated HTML file) out='{check_html_cmd.stdout}', err='{check_html_cmd.stderr}")
            html_output = check_html_cmd.stdout

            allure.attach(html_output, name='generated_html', attachment_type=allure.attachment_type.HTML)

            check.is_in('<title>My Test Document</title>', html_output, 'HTML <title> tag is missing')
            check.is_in('<h2 class=\"title\"><a id=\"id1337\"></a>My Test Document</h2>', html_output, 'HTML <h2> missing')
            check.is_in('<p>This is a paragraph for the transformation test.</p>', html_output, 'HTML <p> tag is missing')
