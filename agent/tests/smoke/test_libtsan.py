import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtsan tests')
@pytest.mark.smoke
@pytest.mark.libtsan
class TestLibtsan:
    '''libtsan smoke test class'''

    @allure.title('libtsan: shared library exists')
    @pytest.mark.minimal
    def test_libtsan_shared_lib(self, ssh_client: SshClient):
        '''Test libtsan shared library installed'''
        with allure.step('Checking libtsan.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libtsan.so')
            assert is_elf, f'libtsan failed: {msg}'
