import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('jansson-dev tests')
@pytest.mark.smoke
@pytest.mark.jansson_dev
class TestJanssonDev:
    '''jansson-dev smoke test class'''

    @allure.title('jansson-dev: development headers test')
    @pytest.mark.minimal
    def test_jansson_headers(self, ssh_client: SshClient):
        '''Test that jansson header files are installed'''
        with allure.step('Checking available headers'):
            cmd = ssh_client.exec(
                'stat /usr/include/jansson.h', ignore_rc=True)
            assert cmd.rc == 0, f"jansson-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('jansson-dev: libraries test')
    @pytest.mark.minimal
    def test_jansson_dev_lib(self, ssh_client: SshClient):
        '''Test jansson-dev libraries installed'''
        with allure.step('Checking jansson-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libjansson.so')
            assert is_elf, f'jansson-dev failed: {msg}'

    @allure.title('jansson-dev: compile and run test')
    def test_jansson_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test jansson library with C program'''
        ssh_client.put_file(
            f'{test_files_path}/test_jansson.c', remote_tmp_path)
        with allure.step('Compiling and running C program with jansson'):
            command = f'gcc {remote_tmp_path}/test_jansson.c -o {remote_tmp_path}/test_jansson -ljansson && {remote_tmp_path}/test_jansson'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'JSON:' in cmd.stdout and 'smoke_test' in cmd.stdout and '42' in cmd.stdout, \
                f"jansson-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
