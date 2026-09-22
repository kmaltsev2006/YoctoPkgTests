import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('python3-cryptography tests')
@pytest.mark.smoke
@pytest.mark.python3_cryptography
class TestPython3Cryptography:
    '''Tests for the python3-cryptography package'''

    @allure.title('python3-cryptography: minimal import test')
    @pytest.mark.minimal
    def test_python3_cryptography_import(self, ssh_client: SshClient):
        '''Test if cryptography module can be imported'''
        with allure.step('Check module import'):
            cmd = ssh_client.exec('python3 -c "import cryptography; print(cryptography.__version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-cryptography failed (Import failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-cryptography: libraries test')
    @pytest.mark.minimal
    def test_python3_cryptography_lib(self, ssh_client: SshClient):
        '''Test cryptography shared objects installed'''
        with allure.step('Checking cryptography shared objects'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/python3*/site-packages/cryptography/hazmat/bindings/_rust*.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('python3-cryptography: functional encryption test')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_cryptography_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests functional cryptography:
        1. Uploads a script that uses Fernet (symmetric encryption).
        2. Runs the script to verify keygen, encryption, and decryption.
        '''
        script_name = 'py3_cryptography.py'
        ssh_client.put_file(
            f'{test_files_path}/py3_cryptography.py', remote_tmp_path)

        with allure.step('Run encryption/decryption script'):
            cmd = ssh_client.exec(f'python3 {remote_tmp_path}/{script_name}', ignore_rc=True)

            check.equal(cmd.rc, 0, f"python3-cryptography failed (Functional script crashed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Cryptography functional test: PASSED', cmd.stdout,
                        f"python3-cryptography failed (Logic verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('python3-cryptography: dependency check')
    @pytest.mark.minimal
    def test_python3_cryptography_deps(self, ssh_client: SshClient):
        '''Verify that cryptography can access OpenSSL backend'''
        with allure.step('Check OpenSSL backend access'):
            cmd = ssh_client.exec('python3 -c "from cryptography.hazmat.backends import openssl; print(openssl.backend.openssl_version_text())"', \
                                   ignore_rc=True)
            assert cmd.rc == 0, f"python3-cryptography failed (OpenSSL backend unavailable): out='{cmd.stdout}', err='{cmd.stderr}'"
