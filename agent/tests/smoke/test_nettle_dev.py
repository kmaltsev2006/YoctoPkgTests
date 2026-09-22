import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib

@allure.suite('nettle-dev tests')
@pytest.mark.smoke
@pytest.mark.nettle_dev
class TestNettleDev:
    '''nettle-dev smoke test class'''

    @allure.title('nettle_dev: check header')
    @pytest.mark.minimal
    def test_nettle_dev_version(self, ssh_client: SshClient):
        '''Testing nettle installed headers'''
        with allure.step('Check nettle headers'):
            cmd = ssh_client.exec('test -e /usr/include/nettle', ignore_rc=True)
            assert cmd.rc == 0, f'nettle headers not found: {cmd.stderr}'

    @allure.title('nettle-dev: check shared libraries')
    @pytest.mark.minimal
    def test_nettle_dev_shared_libraries(self, ssh_client: SshClient):
        '''Testing nettle libraries installed'''
        with allure.step('Check libnettle.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libnettle.so')
            assert is_elf, msg

    # pylint: disable=duplicate-code
    @allure.title('nettle-dev: check static libraries')
    @pytest.mark.minimal
    def test_nettle_dev_static_libraries(self, ssh_client: SshClient):
        '''Testing nettle static libraries installed'''
        with allure.step('Check libnettle.a'):
            is_static_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libnettle.a')
            assert is_static_lib, msg

    # pylint: disable=unused-argument
    @allure.title('nettle_dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_nettle_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing basic functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_nettle.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'gcc {remote_tmp_path}/test_nettle.cpp -lnettle -o \
                                    {remote_tmp_path}/a.out && {remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'nettle-dev is broken: {cmd.stderr}'
