import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libatomic-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libatomic_staticdev
class TestLibatomicStaticdev:
    '''libatomic-staticdev smoke test class'''

    @allure.title('libatomic-staticdev: static library test')
    @pytest.mark.minimal
    def test_libatomic_static_lib(self, ssh_client: SshClient):
        '''Test libatomic-staticdev static library installed'''

        with allure.step('Checking libatomic.a'):
            is_static, msg = check_static_lib(
                ssh_client, '/usr/lib/libatomic.a')
            assert is_static, f'libatomic-staticdev failed: {msg}'

    @allure.title('libatomic-staticdev: functional test')
    def test_libatomic_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing compilation with libatomic'''
        ssh_client.put_file(
            f'{test_files_path}/atomic_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/atomic_test.c'
        test_binary = f'{remote_tmp_path}/atomic_test'

        with allure.step('Compiling and running with libatomic'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -latomic -static && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBATOMIC_FUNCTIONS_WORK' in cmd.stdout, \
                f"libatomic-staticdev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
