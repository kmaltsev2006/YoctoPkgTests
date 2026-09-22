import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib


@allure.suite('e2fsprogs-dev tests')
@pytest.mark.smoke
@pytest.mark.e2fsprogs_dev
class TestE2fsprogsDev:
    '''e2fsprogs-dev smoke test class'''

    @allure.title('e2fsprogs-dev: check shared libraries')
    @pytest.mark.minimal
    def test_e2fsprogs_dev_shared_libraries(self, ssh_client: SshClient):
        '''Check e2fsprogs-dev shared libraries'''
        with allure.step('Check libext2fs.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libext2fs.so')
            assert is_elf, f'e2fsprogs-dev shared library check failed: out="{msg}", err=""'

    @allure.title('e2fsprogs-staticdev: check static libraries')
    @pytest.mark.minimal
    def test_e2fsprogs_dev_static_libraries(self, ssh_client: SshClient):
        '''Check e2fsprogs-staticdev static libraries'''
        with allure.step('Check libext2fs.a'):
            is_static_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libext2fs.a')
            assert is_static_lib, f'e2fsprogs-staticdev static library check failed: out="{msg}", err=""'
