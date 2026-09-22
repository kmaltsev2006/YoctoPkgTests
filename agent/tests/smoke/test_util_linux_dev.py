import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('util-linux-dev tests')
@pytest.mark.smoke
@pytest.mark.util_linux_dev
class TestUtilLinuxDev:
    '''util-linux-dev smoke test class'''

    @allure.title('util-linux-dev: check headers')
    @pytest.mark.minimal
    def test_util_linux_dev_headers(self, ssh_client: SshClient):
        '''Testing util-linux headers installed'''
        with allure.step('Check util-linux headers'):
            # Checking main library headers: libmount, libsmartcols, libblkid, uuid
            cmd = ssh_client.exec('test -e /usr/include/libmount/libmount.h && '
                                 'test -e /usr/include/libsmartcols/libsmartcols.h', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('util-linux-dev: check shared libraries')
    @pytest.mark.minimal
    def test_util_linux_dev_shared_libraries(self, ssh_client: SshClient):
        '''Testing util-linux shared libraries installed'''
        with allure.step('Check libmount.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libmount.so')
            check.equal(is_elf, True, f"util-linux-dev failed (libmount.so check failed) out='{msg}', err=''")

        with allure.step('Check libsmartcols.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libsmartcols.so')
            check.equal(is_elf, True, f"util-linux-dev failed (libsmartcols.so check failed) out='{msg}', err=''")

    # pylint: disable=unused-argument
    @allure.title('util-linux-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_util_linux_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing util-linux libraries workability via compilation'''
        ssh_client.put_file(f'{test_files_path}/test_util_linux_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            # Link against libmount and libsmartcols
            cmd = ssh_client.exec(f'g++ -o {remote_tmp_path}/util_dev_test {remote_tmp_path}/test_util_linux_dev.cpp -lmount -lsmartcols\
&& {remote_tmp_path}/util_dev_test', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-dev failed (compilation or execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('util-linux-dev: check pkg-config')
    def test_util_linux_dev_pkgconfig(self, ssh_client: SshClient):
        '''Check if util-linux pkg-config files exist'''
        with allure.step('Check mount.pc'):
            cmd = ssh_client.exec('pkg-config --exists mount', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-dev failed (pkg-config mount check failed) out='{cmd.stdout}', err='{cmd.stderr}'"
