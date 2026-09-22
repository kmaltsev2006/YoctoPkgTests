import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('libdw tests')
@pytest.mark.smoke
@pytest.mark.libdw
class TestLibdw:
    '''libdw smoke test class'''

    @allure.title('libdw: library test')
    def test_libdw_library(self, ssh_client: SshClient):
        '''Test libdw library installed'''
        with allure.step('Check if libdw.so is a valid ELF file'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libdw.so')
            assert is_elf, msg
