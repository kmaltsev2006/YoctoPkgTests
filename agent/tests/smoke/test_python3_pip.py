import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-pip tests')
@pytest.mark.smoke
@pytest.mark.python3_pip
class TestPython3Pip:
    '''Tests for the python3-pip package (Python Package Installer)'''

    @allure.title('python3-pip: CLI version test')
    @pytest.mark.minimal
    def test_python3_pip_version(self, ssh_client: SshClient):
        '''Test if pip3 utility is available and returns version'''
        with allure.step('Check pip3 version'):
            cmd = ssh_client.exec('pip3 --version', ignore_rc=True)
            assert cmd.rc == 0, f"python3-pip failed (CLI tool not working): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-pip: libraries test')
    @pytest.mark.minimal
    def test_python3_pip_lib(self, ssh_client: SshClient):
        '''Test python3-pip package installation directory'''
        with allure.step('Checking pip package directory'):
            cmd = ssh_client.exec('test -d /usr/lib/python3*/site-packages/pip', ignore_rc=True)
            assert cmd.rc == 0, f"python3-pip failed (Package directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-pip: functional inspection test')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_pip_functional(self, ssh_client: SshClient, are_utils_available: None):
        '''
        Tests functional features of pip (offline mode):
        1. List installed packages.
        2. Show details of the pip package itself.
        '''
        with allure.step('Check pip list output'):
            cmd = ssh_client.exec('pip3 list', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-pip failed (pip list failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('pip', cmd.stdout, f"python3-pip failed (pip not found in list): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Check pip show details'):
            cmd = ssh_client.exec('pip3 show pip', ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-pip failed (pip show failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Name: pip', cmd.stdout, f"python3-pip failed (Wrong metadata): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('python3-pip: binary existence test')
    @pytest.mark.minimal
    def test_python3_pip_bin(self, ssh_client: SshClient):
        '''Check if pip3 binary exists in /usr/bin'''
        with allure.step('Checking /usr/bin/pip3'):
            cmd = ssh_client.exec('test -x /usr/bin/pip3', ignore_rc=True)
            assert cmd.rc == 0, f"python3-pip failed (Binary /usr/bin/pip3 not found or not executable): out='{cmd.stdout}', err='{cmd.stderr}'"
