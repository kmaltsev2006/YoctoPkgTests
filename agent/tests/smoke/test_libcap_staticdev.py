import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libcap-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libcap_staticdev
class TestLibcapStaticdev:
    '''libcap-staticdev smoke test class'''

    @allure.title('libcap-staticdev: static library test')
    @pytest.mark.minimal
    def test_libcap_static_lib(self, ssh_client: SshClient):
        '''Test libcap-staticdev static library installed'''
        with allure.step('Checking libcap.a'):
            is_static, msg = check_static_lib(ssh_client, '/usr/lib/libcap.a')
            assert is_static, f'libcap-staticdev failed: {msg}'

    @allure.title('libcap-staticdev: functional test')
    def test_libcap_staticdev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libcap'''
        ssh_client.put_file(
            f'{test_files_path}/libcap_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libcap_test.c'
        test_binary = f'{remote_tmp_path}/libcap_test'

        with allure.step('Compiling and running with libcap'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -static -lcap && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBCAP_FUNCTIONS_WORK' in cmd.stdout, f"libcap-staticdev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
