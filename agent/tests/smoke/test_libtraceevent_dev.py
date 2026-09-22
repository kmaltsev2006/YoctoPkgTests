import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtraceevent-dev tests')
@pytest.mark.smoke
@pytest.mark.libtraceevent_dev
class TestLibtraceeventDev:
    '''libtraceevent-dev smoke test class'''

    @allure.title('libtraceevent-dev: headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/traceevent/event-utils.h',
        '/usr/include/traceevent/event-parse.h'
    ])
    def test_libtraceevent_dev_headers(self, header, ssh_client: SshClient):
        '''Test libtraceevent-dev headers installed'''
        with allure.step('Checking libtraceevent-dev headers'):
            cmd = ssh_client.exec(
                f'stat {header}',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"libtraceevent-dev failed (headers not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libtraceevent-dev: libraries test')
    @pytest.mark.minimal
    def test_libtraceevent_dev_lib(self, ssh_client: SshClient):
        '''Test libtraceevent-dev libraries installed'''
        with allure.step('Checking libtraceevent-dev libraries'):
            is_elf, msg = check_elf_file(
                ssh_client, '/usr/lib/libtraceevent.so')
            assert is_elf, f'libtraceevent-dev failed: {msg}'

    @allure.title('libtraceevent-dev: compile and link test')
    def test_libtraceevent_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with libtraceevent'''
        ssh_client.put_file(
            f'{test_files_path}/libtraceevent_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/libtraceevent_test.c'
        test_binary = f'{remote_tmp_path}/libtraceevent_test'

        with allure.step('Compiling and running with libtraceevent'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -ltraceevent && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'LIBTRACEEVENT_FUNCTIONS_WORK' in cmd.stdout, f"libtraceevent-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
