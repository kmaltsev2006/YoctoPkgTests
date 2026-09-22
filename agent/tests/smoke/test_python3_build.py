import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-build tests')
@pytest.mark.smoke
@pytest.mark.python3_build
class TestPython3Build:
    '''Tests for the python3-build package (PEP 517 build frontend)'''

    @allure.title('python3-build: minimal version test')
    @pytest.mark.minimal
    def test_python3_build_version(self, ssh_client: SshClient):
        '''Tests if python3-build is installed and returns version'''
        with allure.step('Check build version'):
            cmd = ssh_client.exec('python3 -m build --version', ignore_rc=True)
            assert cmd.rc == 0, f"python3-build failed (Command failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-build: library test')
    @pytest.mark.minimal
    def test_python3_build_lib(self, ssh_client: SshClient):
        '''Test python3-build installation directory'''
        with allure.step('Checking python3-build package directory'):
            cmd = ssh_client.exec('python3 -c "import build; print(build.__file__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-build failed (Python module not importable): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-build: full cycle (project build)')
    @pytest.mark.parametrize('are_utils_available', [['python3', 'wheel']], indirect=True)
    def test_python3_build_full_cycle(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests the full build cycle of a Python package:
        1. Prepares a minimal pyproject.toml.
        2. Runs python3 -m build.
        3. Verifies .whl and .tar.gz creation.
        '''
        project_dir = f'{remote_tmp_path}/test_package'
        ssh_client.create_remote_dir(f'{project_dir}')

        ssh_client.put_file(
            f'{test_files_path}/test_python3_build/pyproject.toml', project_dir)

        with allure.step('Building the Python package'):
            cmd = ssh_client.exec(f'cd {project_dir} && python3 -m build --no-isolation', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-build failed (Build process failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Checking for build artifacts'):
            cmd_sdist = ssh_client.exec(f'ls {project_dir}/dist/*.tar.gz', ignore_rc=True)
            check.equal(cmd_sdist.rc, 0, f"python3-build failed (sdist not found): out='{cmd_sdist.stdout}', err='{cmd_sdist.stderr}'")

            cmd_wheel = ssh_client.exec(f'ls {project_dir}/dist/*.whl', ignore_rc=True)
            check.equal(cmd_wheel.rc, 0, f"python3-build failed (wheel not found): out='{cmd_wheel.stdout}', err='{cmd_wheel.stderr}'")
