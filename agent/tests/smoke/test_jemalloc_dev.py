import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('jemalloc-dev tests')
@pytest.mark.smoke
@pytest.mark.jemalloc_dev
class TestJemallocDev:
    '''jemalloc-dev smoke test class'''

    @allure.title('jemalloc-dev: development headers test')
    @pytest.mark.minimal
    def test_jemalloc_dev_headers(self, ssh_client: SshClient):
        '''Test jemalloc development headers'''
        with allure.step('Check jemalloc headers are installed'):
            cmd = ssh_client.exec(
                'stat /usr/include/jemalloc/jemalloc.h', ignore_rc=True)
            assert cmd.rc == 0, f"jemalloc-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('jemalloc-dev: libraries test')
    @pytest.mark.minimal
    def test_jemalloc_dev_lib(self, ssh_client: SshClient):
        '''Test jemalloc-dev libraries installed'''
        with allure.step('Checking jemalloc-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libjemalloc.so')
            assert is_elf, f'jemalloc-dev failed: {msg}'

    @allure.title('jemalloc-dev: compile and run test')
    def test_jemalloc_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test jemalloc with C program compile and run'''
        ssh_client.put_file(
            f'{test_files_path}/test_jemalloc_dev.c', remote_tmp_path)
        with allure.step('Compiling and running C program with jemalloc lib'):
            command = f'gcc {remote_tmp_path}/test_jemalloc_dev.c -o {remote_tmp_path}/test_jemalloc_dev -ljemalloc && \
                  {remote_tmp_path}/test_jemalloc_dev'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'jemalloc test' in cmd.stdout, f"jemalloc-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
