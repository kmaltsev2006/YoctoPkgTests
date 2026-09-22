import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libtracefs-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libtracefs_staticdev
class TestLibtracefsStaticdev:
    '''libtracefs-staticdev smoke test class'''

    @allure.title('libtracefs-staticdev: static library test')
    @pytest.mark.minimal
    def test_libtracefs_static_lib(self, ssh_client: SshClient):
        '''Test libtracefs-staticdev static library installed'''
        with allure.step('Checking libtracefs static library'):
            is_static, msg = check_static_lib(
                ssh_client, '/usr/lib/libtracefs.a')
            assert is_static, f'libtracefs-staticdev failed: {msg}'

    @allure.title('libtracefs-staticdev: compile and link test')
    def test_libtracefs_staticdev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libtracefs'''
        ssh_client.put_file(
            f'{test_files_path}/libtracefs_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libtracefs_test.c'
        test_binary = f'{remote_tmp_path}/libtracefs_test'

        with allure.step('Compiling and running with libtracefs'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -static -ltracefs -ltraceevent -I /usr/include/traceevent && {test_binary}',
                ignore_rc=True
            )
            success_conditions = [
                'TRACEFS_FOUND',
                'LIBTRACEFS_TEST_PASS'
            ]

            success = any(
                condition in cmd.stdout for condition in success_conditions)
            assert cmd.rc == 0 and success, f"libtracefs-staticdev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
