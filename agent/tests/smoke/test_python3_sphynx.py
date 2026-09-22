import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-sphinx tests')
@pytest.mark.smoke
@pytest.mark.python3_sphinx
class TestPython3Sphinx:
    '''Tests for the python3-sphinx package (Documentation generator)'''

    @allure.title('python3-sphinx: CLI version test')
    @pytest.mark.minimal
    def test_python3_sphinx_version(self, ssh_client: SshClient):
        '''Test if sphinx-build utility is available and returns version'''
        with allure.step('Check sphinx-build version'):
            cmd = ssh_client.exec('sphinx-build --version', ignore_rc=True)
            assert cmd.rc == 0, f"python3-sphinx failed (CLI tool not working): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-sphinx: libraries test')
    @pytest.mark.minimal
    def test_python3_sphinx_lib(self, ssh_client: SshClient):
        '''Test python3-sphinx package directory installation'''
        with allure.step('Checking sphinx package directory'):
            cmd = ssh_client.exec('test -d /usr/lib/python3*/site-packages/sphinx', ignore_rc=True)
            assert cmd.rc == 0, f"python3-sphinx failed (Package directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-sphinx: full build cycle')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_sphinx_full_cycle(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests the full documentation build lifecycle:
        1. Prepares a minimal Sphinx project (conf.py, index.rst).
        2. Runs sphinx-build to generate HTML.
        3. Verifies the output HTML file and its content.
        '''
        src_dir = f'{remote_tmp_path}/sphinx_src'
        build_dir = f'{remote_tmp_path}/sphinx_out'

        ssh_client.create_remote_dir(f'{src_dir}')

        for file in ['index.rst', 'conf.py']:
            ssh_client.put_file(
                f'{test_files_path}/test_python3_sphinx/{file}', src_dir)

        with allure.step('Building HTML documentation'):
            cmd = ssh_client.exec(f'sphinx-build -b html {src_dir} {build_dir}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-sphinx failed (Build process failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verifying output artifacts'):
            output_file = f'{build_dir}/index.html'
            cmd_check = ssh_client.exec(f'test -f {output_file}', ignore_rc=True)
            check.equal(cmd_check.rc, 0, f"python3-sphinx failed (Output HTML not found): out='{cmd_check.stdout}', err='{cmd_check.stderr}'")

            if cmd_check.rc == 0:
                cmd_grep = ssh_client.exec(f'grep "Welcome to Test Docs" {output_file}', ignore_rc=True)
                check.equal(cmd_grep.rc, 0, f"python3-sphinx failed (Expected content not found in HTML): out='{cmd_grep.stdout}', \
                            err='{cmd_grep.stderr}'")

    @allure.title('python3-sphinx: submodules test')
    @pytest.mark.minimal
    def test_python3_sphinx_import(self, ssh_client: SshClient):
        '''Test if sphinx core module can be imported by Python'''
        with allure.step('Check module import'):
            cmd = ssh_client.exec('python3 -c "import sphinx; print(sphinx.__display_version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-sphinx failed (Module import failed): out='{cmd.stdout}', err='{cmd.stderr}'"
