import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libnl-dev tests')
@pytest.mark.smoke
@pytest.mark.libnl_dev
class TestLibNlDev:
    '''Tests covering libnl-dev package (pkg-config and headers).'''

    @allure.title('libnl-dev: libraries test')
    @pytest.mark.minimal
    def test_libnl_dev_lib(self, ssh_client: SshClient):
        '''Test libnl-dev libraries installed'''
        with allure.step('Checking libnl-dev libraries'):
            # Проверяем основную библиотеку libnl-3
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libnl-3.so')
            assert is_elf, msg

    @allure.title('libnl-dev: headers test')
    @pytest.mark.minimal
    def test_libnl_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            # Стандартный путь для заголовков libnl-3
            cmd = ssh_client.exec(
                'test -f /usr/include/libnl3/netlink/netlink.h', ignore_rc=True)
            assert cmd.rc == 0, f"Libnl failed (Header file 'netlink.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"
