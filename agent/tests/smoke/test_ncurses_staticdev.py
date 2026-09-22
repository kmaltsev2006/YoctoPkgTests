import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib

@allure.suite('ncurses-staticdev tests')
@pytest.mark.smoke
@pytest.mark.ncurses_staticdev
class TestNcursesStaticdev:
    '''ncurses-staticdev smoke test class'''

    @allure.title('ncurses_staticdev: check header')
    @pytest.mark.minimal
    def test_ncurses_staticdev_version(self, ssh_client: SshClient):
        '''Testing ncurses installed headers'''
        with allure.step('Check ncurses header'):
            cmd = ssh_client.exec('test -f /usr/include/ncurses.h', ignore_rc=True)
            assert cmd.rc == 0, f'ncurses header not found: {cmd.stderr}'

    # pylint: disable=duplicate-code
    @allure.title('ncurses-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libncurses.a',
                                 'libncurses++.a',
                             ])
    def test_ncurses_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing ncurses static libraries installed'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg
