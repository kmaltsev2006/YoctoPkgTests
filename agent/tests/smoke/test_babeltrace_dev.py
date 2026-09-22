import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('babeltrace-dev tests')
@pytest.mark.smoke
@pytest.mark.babeltrace_dev
class TestBabeltraceDev:
    '''babeltrace-dev smoke test class'''

    @allure.title('babeltrace-dev: headers test')
    @pytest.mark.minimal
    def test_babeltrace_dev_headers(self, ssh_client: SshClient):
        '''Test babeltrace-dev installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'stat /usr/include/babeltrace/babeltrace.h', ignore_rc=True)
            assert cmd.rc == 0, f"babeltrace-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('babeltrace-dev: libraries test')
    @pytest.mark.minimal
    def test_babeltrace_dev_lib(self, ssh_client: SshClient):
        '''Test babeltrace-dev libraries installed'''
        with allure.step('Checking babeltrace-dev libraries'):
            is_elf, msg = check_elf_file(
                ssh_client, '/usr/lib/libbabeltrace.so')
            assert is_elf, f'babeltrace-dev failed: {msg}'

    @allure.title('babeltrace-dev: compile and run test')
    def test_babeltrace_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test program that uses babeltrace'''
        ssh_client.put_file(
            f'{test_files_path}/test_babeltrace.c', remote_tmp_path)
        with allure.step('babeltrace-dev program compilation and run'):
            command = f'gcc {remote_tmp_path}/test_babeltrace.c -o {remote_tmp_path}/test_babeltrace \
                -lbabeltrace && {remote_tmp_path}/test_babeltrace'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'SUCCESS' in cmd.stdout, f"babeltrace-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
