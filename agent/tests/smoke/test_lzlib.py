import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('lzlib tests')
@pytest.mark.smoke
@pytest.mark.lzlib
class TestLzlib:
    '''lzlib smoke test class'''

    @allure.title('lzlib: library test')
    @pytest.mark.minimal
    def test_lzlib_lib(self, ssh_client: SshClient):
        '''Test lzlib library installed'''
        with allure.step('Checking liblz.so library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblz.so')
            assert is_elf, f'lzlib failed: {msg}'
