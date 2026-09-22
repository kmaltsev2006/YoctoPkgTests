import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('libelf tests')
@pytest.mark.smoke
@pytest.mark.libelf
class TestLibelf:
    '''libelf smoke test class'''

    @allure.title('libelf: library test')
    def test_libelf_library(self, ssh_client: SshClient):
        '''Test libelf library installed'''
        with allure.step('Check if libelf.so is a valid ELF file'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libelf.so')
            assert is_elf, msg
