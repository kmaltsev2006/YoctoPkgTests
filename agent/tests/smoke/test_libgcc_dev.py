import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('libgcc-dev tests')
@pytest.mark.smoke
@pytest.mark.libgcc_dev
class TestLibgccDev:
    '''libgcc-dev smoke test class'''

    @allure.title('libgcc-dev: library test')
    @pytest.mark.minimal
    def test_libgcc_dev_library(self, ssh_client: SshClient) -> None:
        '''Test libgcc-dev library installed'''
        with allure.step('Check if libgcc_s.so is a valid ELF file'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libgcc_s.so')
            assert is_elf, msg
