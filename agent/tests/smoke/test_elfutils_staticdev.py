import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('elfutils-staticdev tests')
@pytest.mark.smoke
@pytest.mark.elfutils_staticdev
class TestElfutilsStaticdev:
    '''elfutils-staticdev smoke test class'''

    @allure.title('elfutils-staticdev: check static libraries')
    @pytest.mark.minimal
    def test_elfutils_staticdev_static_libraries(self, ssh_client: SshClient):
        '''Check elfutils-staticdev static libraries'''
        with allure.step('Check libelf.a'):
            is_static_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libelf.a')
            assert is_static_lib, f'elfutils-staticdev static library check failed: out="{msg}", err=""'
