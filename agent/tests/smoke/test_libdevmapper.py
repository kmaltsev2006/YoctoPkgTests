import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('libdevmapper tests')
@pytest.mark.smoke
@pytest.mark.libdevmapper
class TestLibdevmapper:
    '''libdevmapper smoke test class'''

    @allure.title('libdevmapper: library test')
    def test_libdevmapper_library(self, ssh_client: SshClient):
        '''Test libdevmapper library installed'''
        with allure.step('Check if libdevmapper.so is a valid ELF file'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libdevmapper.so')
            assert is_elf, msg

    @allure.title('libdevmapper: dmsetup command test')
    def test_dmsetup_command(self, ssh_client: SshClient):
        '''Test dmsetup command availability'''
        with allure.step('Run dmsetup version or help command'):
            cmd = ssh_client.exec('dmsetup --version 2>&1 || dmsetup --help')
            # Should not be "command not found"
            assert 'command not found' not in cmd.stderr.lower(), f'dmsetup not available: {cmd.stderr}'
