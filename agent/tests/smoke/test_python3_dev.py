import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('python3-dev tests')
@pytest.mark.smoke
@pytest.mark.python3_dev
class TestPython3Dev:
    '''Tests for the python3-dev package (headers and development tools)'''

    @allure.title('python3-dev: config utility test')
    @pytest.mark.minimal
    def test_python3_dev_config(self, ssh_client: SshClient):
        '''Test python3-config utility functionality'''
        with allure.step('Check python3-config cflags'):
            cmd = ssh_client.exec('python3-config --cflags', ignore_rc=True)
            assert cmd.rc == 0, f"python3-dev failed (python3-config failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-dev: headers test')
    @pytest.mark.minimal
    def test_python3_dev_headers(self, ssh_client: SshClient):
        '''Test installed Python headers'''
        with allure.step('Checking Python.h existence'):
            cmd = ssh_client.exec('test -f /usr/include/python3*/Python.h', ignore_rc=True)
            assert cmd.rc == 0, f"python3-dev failed (Header file 'Python.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('python3-dev: libraries test')
    @pytest.mark.minimal
    def test_python3_dev_lib(self, ssh_client: SshClient):
        '''Test python3 development libraries installed'''
        with allure.step('Checking libpython3 shared library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libpython3*.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('python3-dev: compile and embed test')
    @pytest.mark.parametrize('are_utils_available', [['gcc', 'python3']], indirect=True)
    def test_python3_dev_compile_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that a C program can embed Python using dev files:
        1. Compiles a C source using python3-config flags.
        2. Links against libpython.
        3. Runs the resulting binary.
        '''
        source_path = f'{remote_tmp_path}/test_py3_embed.c'
        binary_path = f'{remote_tmp_path}/test_embed_app'

        ssh_client.put_file(
            f'{test_files_path}/test_py3_embed.c', remote_tmp_path)

        with allure.step('Compile C code with python3-config'):
            cflags = ssh_client.exec('python3-config --cflags', ignore_rc=True).stdout.strip()
            ldflags = ssh_client.exec('python3-config --ldflags --embed', ignore_rc=True).stdout.strip()

            compile_cmd = f'gcc {source_path} {cflags} {ldflags} -o {binary_path}'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-dev failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the embedded Python application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"python3-dev failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Python Embedded Success', cmd.stdout,
                        f"python3-dev failed (Unexpected output): out='{cmd.stdout}', err='{cmd.stderr}'")
