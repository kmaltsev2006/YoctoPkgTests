import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('bzip2-dev tests')
@pytest.mark.smoke
@pytest.mark.bzip2_dev
class TestBzip2Dev:
    '''bzip2-dev smoke test class'''

    @allure.title('bzip2-dev: headers test')
    @pytest.mark.minimal
    def test_bzip2_dev_headers(self, ssh_client: SshClient):
        '''Test bzip2-dev installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec('stat /usr/include/bzlib.h', ignore_rc=True)
            assert cmd.rc == 0, f"bzip2-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('bzip2-dev: libraries test')
    @pytest.mark.minimal
    def test_bzip2_dev_lib(self, ssh_client: SshClient):
        '''Test bzip2-dev libraries installed'''
        with allure.step('Checking bzip2-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libbz2.so')
            assert is_elf, f'bzip2-dev failed: {msg}'

    @allure.title('bzip2-dev: headers compile and run test')
    def test_bzip2_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path):
        '''Test program with bzip2'''
        ssh_client.put_file(
            f'{test_files_path}/test_bzip2.c', remote_tmp_path)
        with allure.step('bzip2-dev compilation and run'):
            command = f'gcc {remote_tmp_path}/test_bzip2.c -o {remote_tmp_path}/test_bzip2_dev -lbz2 && {remote_tmp_path}/test_bzip2_dev'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'COMPRESSED' in cmd.stdout, f"bzip2-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
