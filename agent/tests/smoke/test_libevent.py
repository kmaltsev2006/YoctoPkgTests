import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('libevent tests')
@pytest.mark.smoke
@pytest.mark.libevent
class TestLibevent:
    '''libevent smoke test class'''

    @allure.title('libevent: library test')
    def test_libevent_library(self, ssh_client: SshClient) -> None:
        '''Test libevent library installed'''
        with allure.step('Check if libevent.so is a valid ELF file'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libevent.so')
            assert is_elf, msg
