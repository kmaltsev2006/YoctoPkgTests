import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-dnspython tests')
@pytest.mark.smoke
@pytest.mark.python3_dnspython
class TestPython3Dnspython:
    '''Tests for the python3-dnspython package (DNS toolkit)'''

    @allure.title('python3-dnspython: minimal import test')
    @pytest.mark.minimal
    def test_python3_dnspython_import(self, ssh_client: SshClient):
        '''Test if dnspython module and its resolver can be imported'''
        with allure.step('Check module import'):
            cmd = ssh_client.exec('python3 -c "import dns.resolver; print(dns.__version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-dnspython failed (Import failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-dnspython: libraries test')
    @pytest.mark.minimal
    def test_python3_dnspython_lib(self, ssh_client: SshClient):
        '''Test python3-dnspython installation directory existence'''
        with allure.step('Checking dnspython package directory'):
            cmd = ssh_client.exec('test -d /usr/lib/python3*/site-packages/dns', ignore_rc=True)
            assert cmd.rc == 0, f"python3-dnspython failed (Directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-dnspython: functional logic test')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_dnspython_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests functional features of dnspython:
        1. Uploads a script that performs DNS record manipulation.
        2. Executes the script with a manual resolver configuration.
        '''
        script_name = 'py3_dns.py'
        ssh_client.put_file(
            f'{test_files_path}/py3_dns.py', remote_tmp_path)

        with allure.step('Run dnspython functional script'):
            cmd = ssh_client.exec(f'python3 {remote_tmp_path}/{script_name}', ignore_rc=True)

            check.equal(cmd.rc, 0, f"python3-dnspython failed (Script execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('dnspython functional test: PASSED', cmd.stdout,
                        f"python3-dnspython failed (Logic verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('python3-dnspython: configuration files test')
    @pytest.mark.minimal
    def test_python3_dnspython_resolv_conf(self, ssh_client: SshClient):
        '''Check if system resolv.conf exists'''
        with allure.step('Checking /etc/resolv.conf'):
            cmd = ssh_client.exec('test -f /etc/resolv.conf', ignore_rc=True)
            assert cmd.rc == 0, f"python3-dnspython failed (System resolv.conf missing): out='{cmd.stdout}', err='{cmd.stderr}'"
