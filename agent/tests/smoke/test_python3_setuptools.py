import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-setuptools tests')
@pytest.mark.smoke
@pytest.mark.python3_setuptools
class TestPython3Setuptools:
    '''Tests for the python3-setuptools package'''

    @allure.title('python3-setuptools: minimal import test')
    @pytest.mark.minimal
    def test_python3_setuptools_import(self, ssh_client: SshClient):
        '''Test if setuptools and pkg_resources can be imported'''
        with allure.step('Check modules import'):
            cmd = ssh_client.exec('python3 -c "import setuptools; import pkg_resources; print(setuptools.__version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-setuptools failed (Import failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-setuptools: libraries test')
    @pytest.mark.minimal
    def test_python3_setuptools_lib(self, ssh_client: SshClient):
        '''Test python3-setuptools package directory installation'''
        with allure.step('Checking setuptools package directory'):
            cmd = ssh_client.exec('test -d /usr/lib/python3*/site-packages/setuptools', ignore_rc=True)
            assert cmd.rc == 0, f"python3-setuptools failed (Package directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-setuptools: functional metadata generation')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_setuptools_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests functional features of setuptools:
        1. Prepares a minimal setup.py file.
        2. Runs egg_info command to generate package metadata.
        3. Verifies that .egg-info directory and SOURCES.txt are created.
        '''
        project_dir = f'{remote_tmp_path}/test_pkg'
        ssh_client.create_remote_dir(f'{project_dir}')

        ssh_client.put_file(
            f'{test_files_path}/test_python3_setuptools/setup.py', project_dir)

        with allure.step('Run setup.py egg_info'):
            cmd = ssh_client.exec(f'cd {project_dir} && python3 setup.py egg_info', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-setuptools failed (egg_info command failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify metadata creation'):
            cmd = ssh_client.exec(f'ls -d {project_dir}/*.egg-info', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-setuptools failed (Metadata directory not created): out='{cmd.stdout}', err='{cmd.stderr}'")

            cmd = ssh_client.exec(f'test -f {project_dir}/*.egg-info/SOURCES.txt', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-setuptools failed (SOURCES.txt not found): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('python3-setuptools: pkg_resources functionality')
    @pytest.mark.minimal
    def test_python3_setuptools_pkg_resources(self, ssh_client: SshClient):
        '''Test if pkg_resources can list installed distributions'''
        with allure.step('Check pkg_resources working'):
            script = 'import pkg_resources; [print(d.project_name) for d in pkg_resources.working_set]'
            cmd = ssh_client.exec(f'python3 -c "{script}"', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-setuptools failed (pkg_resources failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('setuptools', cmd.stdout, f"python3-setuptools failed (setuptools not found in working_et): out='{cmd.stdout}', \
                        err='{cmd.stderr}'")
