import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libxml2 tests')
@pytest.mark.smoke
@pytest.mark.libxml2
class TestLibxml2:
    '''libxml2 smoke test class'''

    @allure.title('libxml2: binary test')
    @pytest.mark.minimal
    def test_libxml2_binary(self, ssh_client: SshClient):
        '''Test libxml2 binaries installed'''
        with allure.step('Checking xmlcatalog binary'):
            cmd = ssh_client.exec(
                'which xmlcatalog',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'xmlcatalog not found: {cmd.stderr}'

    @allure.title('libxml2: libraries test')
    @pytest.mark.minimal
    def test_libxml2_lib(self, ssh_client: SshClient):
        '''Test libxml2 libraries installed'''
        with allure.step('Checking libxml2 libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libxml2.so')
            assert is_elf, msg
