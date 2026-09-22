import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('liburcu tests')
@pytest.mark.smoke
@pytest.mark.liburcu
class TestLiburcu:
    '''liburcu smoke tests'''

    @allure.title('liburcu: shared library presence')
    @pytest.mark.minimal
    def test_shared_library(self, ssh_client: SshClient):
        '''Check that liburcu shared library exists and is a valid ELF file'''
        with allure.step('Checking liburcu shared library presence and format'):
            cmd = ssh_client.exec(
                'test -f /usr/lib/liburcu.so',
                ignore_rc=True
            )

            assert cmd.rc == 0, f'liburcu failed (shared library not found): out="{cmd.stdout}", err="{cmd.stderr}"'

            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liburcu.so')
            assert is_elf, f'liburcu failed (invalid ELF shared library): {msg}'
