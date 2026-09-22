import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('popt-dev tests')
@pytest.mark.smoke
@pytest.mark.popt_dev
class TestPoptDev:
    '''popt-dev smoke test class'''

    @allure.title('popt-dev: headers test')
    @pytest.mark.minimal
    def test_popt_dev_headers(self, ssh_client: SshClient):
        '''Test popt-dev installed headers'''
        with allure.step('Checking popt.h header'):
            cmd = ssh_client.exec('stat /usr/include/popt.h', ignore_rc=True)
            assert cmd.rc == 0, f"popt-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('popt-dev: libraries test')
    @pytest.mark.minimal
    def test_popt_dev_lib(self, ssh_client: SshClient):
        '''Test popt-dev libraries installed'''
        with allure.step('Checking libpopt.so library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libpopt.so')
            assert is_elf, f'popt-dev failed: {msg}'

    @allure.title('popt-dev: compile and run test')
    def test_popt_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test popt library functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_popt_dev.c', remote_tmp_path)
        with allure.step('Compiling and running popt test program'):
            command = f'gcc {remote_tmp_path}/test_popt_dev.c -o {remote_tmp_path}/test_popt_dev -lpopt && {remote_tmp_path}/test_popt_dev --help'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0, f"popt-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
