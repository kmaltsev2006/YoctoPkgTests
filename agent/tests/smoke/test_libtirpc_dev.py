import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtirpc-dev tests')
@pytest.mark.smoke
@pytest.mark.libtirpc_dev
class TestLibtirpcDev:
    '''libtirpc-dev smoke test class'''

    @allure.title('libtirpc-dev: headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/tirpc/rpc/rpc.h',
        '/usr/include/tirpc/rpc/types.h',
        '/usr/include/tirpc/netconfig.h'
    ])
    def test_libtirpc_dev_headers(self, header, ssh_client: SshClient):
        '''Test libtirpc-dev headers installed'''
        with allure.step(f'Checking {header}'):
            cmd = ssh_client.exec(f'stat {header}', ignore_rc=True)
            assert cmd.rc == 0, f"libtirpc-dev failed (headers not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libtirpc-dev: libraries test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', [
        '/usr/lib/libtirpc.so',
        '/usr/lib/libtirpc.so.3'
    ])
    def test_libtirpc_dev_libs(self, lib, ssh_client: SshClient):
        '''Test libtirpc-dev libraries installed'''
        with allure.step(f'Checking {lib}'):
            is_elf, msg = check_elf_file(ssh_client, lib)
            assert is_elf, f'libtirpc-dev failed: {msg}'

    @allure.title('libtirpc-dev: compile and link test')
    def test_libtirpc_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libtirpc'''
        ssh_client.put_file(
            f'{test_files_path}/libtirpc_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libtirpc_test.c'
        test_binary = f'{remote_tmp_path}/libtirpc_test'

        with allure.step('Compiling and running with libtirpc'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -ltirpc -I/usr/include/tirpc && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBTIRPC_FUNCTIONS_WORK' in cmd.stdout, f"libtirpc-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
