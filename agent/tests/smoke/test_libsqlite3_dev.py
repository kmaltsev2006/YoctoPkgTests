import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libsqlite3-dev tests')
@pytest.mark.smoke
@pytest.mark.libsqlite3_dev
class TestLibSqlite3Dev:
    '''Tests covering libsqlite3-dev package (headers and configs).'''

    @allure.title('libsqlite3-dev: libraries test')
    @pytest.mark.minimal
    def test_libsqlite3_dev_lib(self, ssh_client: SshClient):
        '''Test libsqlite3-dev libraries installed'''
        with allure.step('Checking libsqlite3-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libsqlite3.so')
            assert is_elf, msg

    @allure.title('libsqlite3-dev: headers test')
    @pytest.mark.minimal
    def test_libsqlite3_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/sqlite3.h', ignore_rc=True)
            assert cmd.rc == 0, f"Libsqlite3-dev failed (Header file 'sqlite3.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"
