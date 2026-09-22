import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('python3-pyyaml tests')
@pytest.mark.smoke
@pytest.mark.python3_pyyaml
class TestPython3Pyyaml:
    '''Tests for the python3-pyyaml package (YAML parser and emitter)'''

    @allure.title('python3-pyyaml: minimal import test')
    @pytest.mark.minimal
    def test_python3_pyyaml_import(self, ssh_client: SshClient):
        '''Test if yaml module can be imported'''
        with allure.step('Check module import'):
            cmd = ssh_client.exec('python3 -c "import yaml; print(yaml.__version__)"', ignore_rc=True)
            assert cmd.rc == 0, f"python3-pyyaml failed (Import failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-pyyaml: libraries test')
    @pytest.mark.minimal
    def test_python3_pyyaml_lib(self, ssh_client: SshClient):
        '''Test pyyaml shared objects installed'''
        with allure.step('Checking pyyaml C-extension'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/python3*/site-packages/yaml/_yaml*.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('python3-pyyaml: functional logic test')
    @pytest.mark.parametrize('are_utils_available', [['python3']], indirect=True)
    def test_python3_pyyaml_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests functional features of PyYAML:
        1. Uploads a script that performs YAML dumping and safe loading.
        2. Executes the script to verify data integrity.
        '''
        script_name = 'py3_yaml.py'
        ssh_client.put_file(
            f'{test_files_path}/py3_yaml.py', remote_tmp_path)

        with allure.step('Run pyyaml functional script'):
            cmd = ssh_client.exec(f'python3 {remote_tmp_path}/{script_name}', ignore_rc=True)

            check.equal(cmd.rc, 0, f"python3-pyyaml failed (Script execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('pyyaml functional test: PASSED', cmd.stdout,
                        f"python3-pyyaml failed (Logic verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
