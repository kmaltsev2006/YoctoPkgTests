import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libtirpc-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libtirpc_staticdev
class TestLibtirpcStaticdev:
    '''libtirpc-staticdev smoke test class'''

    @allure.title('libtirpc-staticdev: static library test')
    @pytest.mark.minimal
    def test_libtirpc_static_lib(self, ssh_client: SshClient):
        '''Test libtirpc-staticdev static library installed'''
        with allure.step('Checking libtirpc static library'):
            is_static, msg = check_static_lib(
                ssh_client, '/usr/lib/libtirpc.a')
            assert is_static, f'libtirpc-staticdev failed: {msg}'

    @allure.title('libtirpc-staticdev: compile with static library test')
    def test_libtirpc_static_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing static linkage with libtirpc'''
        ssh_client.put_file(
            f'{test_files_path}/libtirpc_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libtirpc_test.c'
        test_binary = f'{remote_tmp_path}/libtirpc_test'

        with allure.step('Compiling and running with static libtirpc'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -static -ltirpc -I/usr/include/tirpc && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBTIRPC_FUNCTIONS_WORK' in cmd.stdout, f"libtirpc-staticdev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
