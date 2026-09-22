import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-markdown tests')
@pytest.mark.smoke
@pytest.mark.python3_markdown
class TestPython3Markdown:
    '''Tests for the python3-markdown package'''

    @allure.title('python3-markdown: CLI version test')
    @pytest.mark.minimal
    def test_python3_markdown_cli_version(self, ssh_client: SshClient):
        '''Test if markdown_py utility is available and returns version'''
        with allure.step('Check markdown_py version'):
            cmd = ssh_client.exec('markdown_py --version', ignore_rc=True)
            assert cmd.rc == 0, f"python3-markdown failed (CLI tool not working): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-markdown: libraries test')
    @pytest.mark.minimal
    def test_python3_markdown_lib(self, ssh_client: SshClient):
        '''Test python3-markdown package installation'''
        with allure.step('Checking markdown package directory'):
            cmd = ssh_client.exec('test -d /usr/lib/python3*/site-packages/markdown', ignore_rc=True)
            assert cmd.rc == 0, f"python3-markdown failed (Package directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-markdown: full cycle (CLI and API)')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_markdown_full_cycle(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests the full lifecycle of Markdown conversion:
        1. CLI: Convert .md file to .html.
        2. API: Run python script to verify internal logic.
        '''
        md_file = f'{remote_tmp_path}/test.md'
        html_file = f'{remote_tmp_path}/test.html'
        script_name = 'py3_markdown.py'

        ssh_client.exec(f"echo '# Header' > {md_file}")
        ssh_client.put_file(
            f'{test_files_path}/{script_name}', remote_tmp_path)

        with allure.step('Convert Markdown via CLI'):
            cmd = ssh_client.exec(f'markdown_py {md_file} -f {html_file}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-markdown failed (CLI conversion failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify CLI output'):
            cmd = ssh_client.exec(f'grep "<h1>Header</h1>" {html_file}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-markdown failed (CLI output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run Markdown API functional script'):
            cmd = ssh_client.exec(f'python3 {remote_tmp_path}/{script_name}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-markdown failed (API script failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Markdown API test: PASSED', cmd.stdout,
                        f"python3-markdown failed (Unexpected API output): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('python3-markdown: import test')
    @pytest.mark.minimal
    def test_python3_markdown_import(self, ssh_client: SshClient):
        '''Test if markdown module can be imported by Python'''
        with allure.step('Check module import'):
            cmd = ssh_client.exec('python3 -c "import markdown; print(markdown.__version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-markdown failed (Module import failed): out='{cmd.stdout}', err='{cmd.stderr}'"
