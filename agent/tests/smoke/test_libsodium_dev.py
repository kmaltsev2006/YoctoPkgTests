import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libsodium-dev tests')
@pytest.mark.smoke
@pytest.mark.libsodium_dev
class TestLibSodiumDev:
    '''Tests covering libsodium-dev package (headers and configs).'''

    @allure.title('libsodium-dev: libraries test')
    @pytest.mark.minimal
    def test_libsodium_dev_lib(self, ssh_client: SshClient):
        '''Test libsodium-dev libraries installed'''
        with allure.step('Checking libsodium-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libsodium.so')
            assert is_elf, msg

    @allure.title('libsodium-dev: headers test')
    @pytest.mark.minimal
    def test_libsodium_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/sodium.h', ignore_rc=True)
            assert cmd.rc == 0, f"Libsodium-dev failed (Header file 'sodium.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"
