import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('boost-sml-dev tests')
@pytest.mark.smoke
@pytest.mark.boost_sml_dev
class TestBoostSmlDev:
    '''boost-sml-dev smoke test class'''

    @allure.title('boost_sml_dev: check header')
    @pytest.mark.minimal
    def test_boost_sml_dev_version(self, ssh_client: SshClient):
        '''Testing boost sml installed headers'''
        with allure.step('Check boost_sml_dev header'):
            cmd = ssh_client.exec(
                "cat /usr/include/boost/sml.hpp | grep '#define BOOST_SML_VERSION'", ignore_rc=True)
            assert cmd.rc == 0, f'boost-sml-dev not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('boost_sml_dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_boost_sml_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing basic functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_boost_sml.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'g++ -std=c++17 -O2 -fno-exceptions -Wall -Wextra -Werror \
                                   -pedantic {remote_tmp_path}/test_boost_sml.cpp -o \
                                    {remote_tmp_path}/a.out && {remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'boost-sml-dev is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
