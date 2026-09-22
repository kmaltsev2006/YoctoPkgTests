import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib
from boost_constants import BOOST_STATIC_LIBS


@allure.suite('boost-staticdev tests')
@pytest.mark.smoke
@pytest.mark.boost_staticdev
class TestBoostStaticdev:
    '''boost-staticdev smoke test class'''

    @allure.title('boost-staticdev: check headers')
    @pytest.mark.minimal
    def test_boost_staticdev_headers(self, ssh_client: SshClient):
        '''Testing boost installed headers'''
        with allure.step('Check boost-staticdev headers'):
            cmd = ssh_client.exec('test -e /usr/include/boost', ignore_rc=True)
            assert cmd.rc == 0, f'boost headers not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=duplicate-code
    @allure.title('boost-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             BOOST_STATIC_LIBS)
    def test_boost_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing boost static libraries'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, f'boost static library check failed: out="{msg}", err=""'

    # pylint: disable=unused-argument
    @allure.title('boost-staticdev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_boost_staticdev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing boost basic functionality'''

        ssh_client.put_file(
            f'{test_files_path}/test_boost.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'g++ -o {remote_tmp_path}/a.out {remote_tmp_path}/test_boost.cpp \
                    -static -lboost_filesystem -lboost_system -lboost_thread -lboost_chrono \
                                   -lboost_atomic -lpthread && {remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'boost-staticdev is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
