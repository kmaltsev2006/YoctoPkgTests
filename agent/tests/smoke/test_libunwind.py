import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libunwind tests')
@pytest.mark.smoke
@pytest.mark.libunwind
class TestLibunwind:
    '''libunwind smoke test class'''

    @allure.title('libunwind: shared library presence test')
    @pytest.mark.minimal
    def test_libunwind_library(self, ssh_client: SshClient):
        '''Test that libunwind shared library is installed'''
        with allure.step('Checking libunwind shared library'):
            is_elf, msg = check_elf_file(
                ssh_client,
                '/usr/lib/libunwind.so'
            )
            assert is_elf, f'libunwind failed (shared library ELF check): {msg}'
