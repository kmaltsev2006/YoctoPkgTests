import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib


@allure.suite('elfutils-dev tests')
@pytest.mark.smoke
@pytest.mark.elfutils_dev
class TestElfutilsDev:
    '''elfutils-dev smoke test class'''

    @allure.title('elfutils-dev: check shared libraries')
    @pytest.mark.minimal
    def test_elfutils_dev_shared_libraries(self, ssh_client: SshClient):
        '''Check elfutils-dev shared libraries'''
        with allure.step('Check libelf.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libelf.so')
            assert is_elf, f'elfutils-dev shared library check failed: out="{msg}", err=""'

    @allure.title('e2fsprogs-dev: check static libraries')
    @pytest.mark.minimal
    def test_elfutils_dev_static_libraries(self, ssh_client: SshClient):
        '''Check e2fsprogs-dev static libraries'''
        with allure.step('Check libelf.a'):
            is_static_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libelf.a')
            assert is_static_lib, f'elfutils-dev static library check failed: out="{msg}", err=""'
