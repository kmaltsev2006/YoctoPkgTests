import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtraceevent tests')
@pytest.mark.smoke
@pytest.mark.libtraceevent
class TestLibtraceevent:
    '''libtraceevent smoke test class'''

    @allure.title('libtraceevent: library exists')
    @pytest.mark.minimal
    def test_libtraceevent_lib(self, ssh_client: SshClient):
        '''Test libtraceevent library installed'''
        with allure.step('Checking libtraceevent library'):
            is_elf, msg = check_elf_file(
                ssh_client, '/usr/lib/libtraceevent.so')
            assert is_elf, f'libtraceevent failed: {msg}'
