import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libbsd-dev tests')
@pytest.mark.smoke
@pytest.mark.libbsd_dev
class TestLibbsdDev:
    '''libbsd-dev smoke test class'''

    @allure.title('libbsd-dev: headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/bsd/string.h',
        '/usr/include/bsd/stdlib.h'
    ])
    def test_libbsd_dev_headers(self, header, ssh_client: SshClient):
        '''Test libbsd-dev headers installed'''
        with allure.step(f'Checking {header}'):
            cmd = ssh_client.exec(f'stat {header}', ignore_rc=True)
            assert cmd.rc == 0, f"libbsd-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libbsd-dev: libraries test')
    @pytest.mark.minimal
    def test_libbsd_dev_lib(self, ssh_client: SshClient):
        '''Test libbsd-dev libraries installed'''
        with allure.step('Checking libbsd-dev libraries'):
            cmd = ssh_client.exec('stat /usr/lib/libbsd.so')
            assert cmd.rc == 0, f"libbsd-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libbsd-dev: functional test')
    def test_libbsd_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libbsd'''
        ssh_client.put_file(
            f'{test_files_path}/libbsd_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libbsd_test.c'
        test_binary = f'{remote_tmp_path}/libbsd_test'

        with allure.step('Compiling and running with libbsd'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -lbsd && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBBSD_FUNCTIONS_WORK' in cmd.stdout, f"libbsd-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
