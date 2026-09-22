import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('automake tests')
@pytest.mark.smoke
@pytest.mark.automake
class TestAutomake:
    '''automake smoke test class'''

    @allure.title('automake: version test')
    @pytest.mark.minimal
    def test_automake_version(self, ssh_client: SshClient):
        '''Checking automake installed version'''
        with allure.step('Checking automake version'):
            cmd = ssh_client.exec('automake --version')
            assert cmd.rc == 0, f"automake failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('automake: basic functionality test')
    @pytest.mark.minimal
    def test_automake_basics(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing automake creating configure files'''
        files = ['configure.ac', 'Makefile.am', 'hello.c']
        for file in files:
            ssh_client.put_file(
                f'{test_files_path}/test_automake/{file}', remote_tmp_path)
        with allure.step('Testing automake command'):
            command = f'cd {remote_tmp_path} && aclocal && autoconf && automake --add-missing --copy'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0, f"automake failed: out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('automake: built binary test')
    def test_automake_built_binary(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing automake building executable'''
        files = ['configure.ac', 'Makefile.am', 'hello.c']
        for file in files:
            ssh_client.put_file(
                f'{test_files_path}/test_automake/{file}', remote_tmp_path)
        with allure.step('Testing automake command'):
            command = f'cd {remote_tmp_path} && aclocal && autoconf && automake --add-missing --copy && ./configure && make && ./hello'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'Hello automake test' in cmd.stdout, f"automake failed: out='{cmd.stdout}', err='{cmd.stderr}'"
