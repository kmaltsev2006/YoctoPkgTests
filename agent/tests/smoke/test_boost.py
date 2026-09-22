import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib
from boost_constants import BOOST_SHARED_LIBS, BOOST_STATIC_LIBS


@allure.suite('boost tests')
@pytest.mark.smoke
@pytest.mark.boost
class TestBoost:
    '''boost smoke test class'''

    @allure.title('boost: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             BOOST_SHARED_LIBS)
    def test_boost_shared_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing boost libraries installed'''
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f'boost shared library check failed: out="{msg}", err=""'

    @allure.title('boost: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             BOOST_STATIC_LIBS)
    def test_boost_static_libraries(self, lib: str, ssh_client: SshClient):
        '''TEsting boost static libraries installed'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, f'boost static library check failed: out="{msg}", err=""'
