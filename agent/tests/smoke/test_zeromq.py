import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('zeromq tests')
@pytest.mark.smoke
@pytest.mark.zeromq
class TestZeroMq:
    '''zeromq smoke test class'''

    @allure.title('zeromq: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libzmq.so'])
    def test_zeromq_dev_shared_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing zeromq shared libraries installed'''
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f"zeromq failed (shared library {lib} check failed): '{msg}'"
