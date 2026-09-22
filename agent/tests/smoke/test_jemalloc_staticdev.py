import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('jemalloc-staticdev tests')
@pytest.mark.smoke
@pytest.mark.jemalloc_staticdev
class TestJemallocStaticdev:
    '''jemalloc-staticdev smoke test class'''

    @allure.title('jemalloc-staticdev: staticdevelopment headers test')
    @pytest.mark.minimal
    def test_jemalloc_staticdev_headers(self, ssh_client: SshClient):
        '''Test jemalloc headers'''
        with allure.step('Check jemalloc headers are installed'):
            cmd = ssh_client.exec(
                'stat /usr/include/jemalloc/jemalloc.h', ignore_rc=True)
            assert cmd.rc == 0, f"jemalloc-staticdev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('jemalloc-staticdev: libraries test')
    @pytest.mark.minimal
    def test_jemalloc_staticdev_lib(self, ssh_client: SshClient):
        '''Test jemalloc-staticdev libraries installed'''
        with allure.step('Checking jemalloc-staticdev libraries'):
            is_static, msg = check_static_lib(
                ssh_client, '/usr/lib/libjemalloc.a')
            assert is_static, f'jemalloc-staticdev failed: {msg}'

    @allure.title('jemalloc-staticdev: compile and run test')
    def test_jemalloc_staticdev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test jemalloc with C program compile and run'''
        ssh_client.put_file(
            f'{test_files_path}/test_jemalloc_dev.c', remote_tmp_path)
        with allure.step('Compiling and running C program with jemalloc lib'):
            command = f'gcc {remote_tmp_path}/test_jemalloc_dev.c -o {remote_tmp_path}/test_jemalloc_staticdev \
                  -ljemalloc -static && {remote_tmp_path}/test_jemalloc_staticdev'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'jemalloc test' in cmd.stdout, f"jemalloc-staticdev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
