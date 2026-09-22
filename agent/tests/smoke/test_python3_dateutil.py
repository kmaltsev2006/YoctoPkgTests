import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-dateutil tests')
@pytest.mark.smoke
@pytest.mark.python3_dateutil
class TestPython3Dateutil:
    '''Tests for the python3-dateutil package'''

    @allure.title('python3-dateutil: minimal import test')
    @pytest.mark.minimal
    def test_python3_dateutil_import(self, ssh_client: SshClient):
        '''Test if dateutil module and its components can be imported'''
        with allure.step('Check module import'):
            cmd = ssh_client.exec('python3 -c "import dateutil; from dateutil import parser, relativedelta; print(dateutil.__version__)"',\
                                  ignore_rc=True)
            assert cmd.rc == 0, f"python3-dateutil failed (Import failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-dateutil: package structure test')
    @pytest.mark.minimal
    def test_python3_dateutil_lib(self, ssh_client: SshClient):
        '''Test python3-dateutil installation directory existence'''
        with allure.step('Checking dateutil package directory'):
            cmd = ssh_client.exec('test -d /usr/lib/python3*/site-packages/dateutil', ignore_rc=True)
            assert cmd.rc == 0, f"python3-dateutil failed (Directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-dateutil: functional logic test')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_dateutil_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests functional features of dateutil:
        1. Uploads a script that uses parser and relativedelta.
        2. Executes the script to verify date arithmetic and parsing.
        '''
        script_name = 'py3_dateutil.py'
        ssh_client.put_file(
            f'{test_files_path}/{script_name}', remote_tmp_path)

        with allure.step('Run dateutil functional script'):
            cmd = ssh_client.exec(f'python3 {remote_tmp_path}/{script_name}', ignore_rc=True)

            check.equal(cmd.rc, 0, f"python3-dateutil failed (Script execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('dateutil functional test: PASSED', cmd.stdout,
                        f"python3-dateutil failed (Logic verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('python3-dateutil: dependencies test')
    @pytest.mark.minimal
    def test_python3_dateutil_deps(self, ssh_client: SshClient):
        '''Test if dateutil can access six (common dependency)'''
        with allure.step('Checking six dependency'):
            # dateutil must need six for compability
            cmd = ssh_client.exec('python3 -c "import six; print(six.__version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-dateutil failed (Dependency six not found): out='{cmd.stdout}', err='{cmd.stderr}'"
