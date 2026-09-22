import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('clang-dev tests')
@pytest.mark.smoke
@pytest.mark.clang_dev
class TestClangDev:
    '''clang-dev smoke test class'''

    @allure.title('clang-dev: check installation')
    @pytest.mark.minimal
    def test_clang_dev_version(self, ssh_client: SshClient):
        '''Testing clang-dev installed'''
        with allure.step('Check clang-dev installation'):
            cmd = ssh_client.exec('which clang', ignore_rc=True)
            assert cmd.rc == 0, f'clang-dev not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('clang-dev: check headers')
    @pytest.mark.minimal
    def test_clang_dev_headers(self, ssh_client: SshClient):
        '''Testing clang-dev headers'''
        with allure.step('Check clang-dev headers'):
            cmd = ssh_client.exec('test -e /usr/include/clang', ignore_rc=True)
            assert cmd.rc == 0, f'clang headers not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('clang-dev: check shared libraries')
    @pytest.mark.minimal
    def test_clang_dev_shared_library(self, ssh_client: SshClient):
        with allure.step('Checking libclang library'):
            is_elf, msg = check_elf_file(
                ssh_client, '/usr/lib/libclang-14.so.14.0.0')
            assert is_elf, f'libclang check failed: out="{msg}", err=""'
