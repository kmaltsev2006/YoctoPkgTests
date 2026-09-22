import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libcap-dev tests')
@pytest.mark.smoke
@pytest.mark.libcap_dev
class TestLibcapDev:
    '''libcap-dev smoke test class'''

    @allure.title('libcap-dev: headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/sys/capability.h',
        '/usr/include/cap-ng.h'
    ])
    def test_libcap_dev_headers(self, header, ssh_client: SshClient):
        '''Test libcap-dev headers installed'''
        with allure.step(f'Checking {header}'):
            cmd = ssh_client.exec(f'stat {header}', ignore_rc=True)
            assert cmd.rc == 0, f"libcap-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libcap-dev: libraries test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', [
        '/usr/lib/libcap.so',
        '/usr/lib/libcap-ng.so'
    ])
    def test_libcap_dev_libs(self, lib, ssh_client: SshClient):
        '''Test libcap-dev libraries installed'''
        with allure.step(f'Checking {lib}'):
            is_elf, msg = check_elf_file(ssh_client, lib)
            assert is_elf, f'libcap-dev failed: {msg}'

    @allure.title('libcap-dev: functional test')
    def test_libcap_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libcap'''
        ssh_client.put_file(
            f'{test_files_path}/libcap_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libcap_test.c'
        test_binary = f'{remote_tmp_path}/libcap_test'

        with allure.step('Compiling and running with libcap'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -lcap && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBCAP_FUNCTIONS_WORK' in cmd.stdout, f"libcap-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
