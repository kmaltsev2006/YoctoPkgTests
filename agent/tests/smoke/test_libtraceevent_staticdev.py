import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libtraceevent-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libtraceevent_staticdev
class TestLibtraceeventStaticdev:
    '''libtraceevent-staticdev smoke test class'''

    @allure.title('libtraceevent-staticdev: static library test')
    @pytest.mark.minimal
    def test_libtraceevent_static_lib(self, ssh_client: SshClient):
        '''Test libtraceevent-staticdev static library installed'''
        with allure.step('Checking libtraceevent static library'):
            is_static, msg = check_static_lib(
                ssh_client, '/usr/lib/libtraceevent.a')
            assert is_static, f'libtraceevent-staticdev failed: {msg}'

    @allure.title('libtraceevent-staticdev: compile and link test')
    def test_libtraceevent_staticdev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libtraceevent'''
        ssh_client.put_file(
            f'{test_files_path}/libtraceevent_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libtraceevent_test.c'
        test_binary = f'{remote_tmp_path}/libtraceevent_test'

        with allure.step('Compiling and running with libtraceevent'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -static -ltraceevent && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBTRACEEVENT_FUNCTIONS_WORK' in cmd.stdout, \
                f"libtraceevent-staticdev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
