import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('util-linux-libuuid-dev tests')
@pytest.mark.smoke
@pytest.mark.util_linux_libuuid_dev
class TestUtilLinuxLibuuidDev:
    '''util-linux-libuuid-dev smoke test class'''

    @allure.title('util-linux-libuuid-dev: check headers')
    @pytest.mark.minimal
    def test_util_linux_libuuid_dev_headers(self, ssh_client: SshClient):
        '''Testing libuuid headers installed'''
        with allure.step('Check uuid/uuid.h'):
            cmd = ssh_client.exec('test -e /usr/include/uuid/uuid.h', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-libuuid-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('util-linux-libuuid-dev: check shared library')
    @pytest.mark.minimal
    def test_util_linux_libuuid_dev_shared_library(self, ssh_client: SshClient):
        '''Testing libuuid shared library link installed'''
        with allure.step('Check libuuid.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libuuid.so')
            assert is_elf, f"util-linux-libuuid-dev failed (libuuid.so check failed) out='{msg}', err=''"

    # pylint: disable=unused-argument
    @allure.title('util-linux-libuuid-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_util_linux_libuuid_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing libuuid workability via compilation'''
        ssh_client.put_file(f'{test_files_path}/test_util_linux_libuuid_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'g++ -o {remote_tmp_path}/uuid_test {remote_tmp_path}/test_util_linux_libuuid_dev.cpp -luuid\
&& {remote_tmp_path}/uuid_test', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-libuuid-dev failed (compilation or execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('util-linux-libuuid-dev: check pkg-config')
    def test_util_linux_libuuid_dev_pkgconfig(self, ssh_client: SshClient):
        '''Check if uuid pkg-config file exists'''
        with allure.step('Check uuid.pc'):
            cmd = ssh_client.exec('pkg-config --exists uuid', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-libuuid-dev failed (pkg-config uuid check failed) out='{cmd.stdout}', err='{cmd.stderr}'"
