import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('python3-pyasn1 tests')
@pytest.mark.smoke
@pytest.mark.python3_pyasn1
class TestPython3Pyasn1:
    '''Tests for the python3-pyasn1 package (ASN.1 library)'''

    @allure.title('python3-pyasn1: minimal import test')
    @pytest.mark.minimal
    def test_python3_pyasn1_import(self, ssh_client: SshClient):
        '''Test if pyasn1 module can be imported'''
        with allure.step('Check module import'):
            cmd = ssh_client.exec('python3 -c "import pyasn1; print(pyasn1.__version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-pyasn1 failed (Import failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-pyasn1: libraries test')
    @pytest.mark.minimal
    def test_python3_pyasn1_lib(self, ssh_client: SshClient):
        '''Test python3-pyasn1 package directory installation'''
        with allure.step('Checking pyasn1 package directory'):
            cmd = ssh_client.exec('test -d /usr/lib/python3*/site-packages/pyasn1', ignore_rc=True)
            assert cmd.rc == 0, f"python3-pyasn1 failed (Package directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('python3-pyasn1: functional codec test')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_pyasn1_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests functional features of pyasn1:
        1. Uploads a script that performs BER encoding and decoding.
        2. Executes the script to verify ASN.1 types and codecs integrity.
        '''
        script_name = 'py3_pyasn1.py'
        ssh_client.put_file(
            f'{test_files_path}/py3_pyasn1.py', remote_tmp_path)

        with allure.step('Run pyasn1 functional script'):
            cmd = ssh_client.exec(f'python3 {remote_tmp_path}/{script_name}', ignore_rc=True)

            check.equal(cmd.rc, 0, f"python3-pyasn1 failed (Script execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('pyasn1 functional test: PASSED', cmd.stdout,
                        f"python3-pyasn1 failed (Logic verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('python3-pyasn1: submodules test')
    @pytest.mark.minimal
    def test_python3_pyasn1_submodules(self, ssh_client: SshClient):
        '''Test if key submodules (codec, type) are available'''
        with allure.step('Check submodules import'):
            cmd = ssh_client.exec('python3 -c "from pyasn1.codec.ber import encoder; from pyasn1.type import univ"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-pyasn1 failed (Submodules import failed): out='{cmd.stdout}', err='{cmd.stderr}'"
