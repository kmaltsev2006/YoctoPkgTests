import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtracefs tests')
@pytest.mark.smoke
@pytest.mark.libtracefs
class TestLibtracefs:
    '''libtracefs smoke test class'''

    @allure.title('libtracefs: library exists')
    @pytest.mark.minimal
    def test_libtracefs_lib(self, ssh_client: SshClient):
        '''Test libtracefs library installed'''
        with allure.step('Checking libtracefs library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libtracefs.so')
            assert is_elf, f'libtracefs failed: {msg}'
