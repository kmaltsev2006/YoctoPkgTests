import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libasan tests')
@pytest.mark.smoke
@pytest.mark.libasan
class TestLibasan:
    '''libasan smoke test class'''

    @allure.title('libasan: shared library exists')
    @pytest.mark.minimal
    def test_libasan_shared_lib(self, ssh_client: SshClient):
        '''Test libasan shared library installed'''
        with allure.step('Checking libasan.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libasan.so')
            assert is_elf, f'libasan failed: {msg}'
