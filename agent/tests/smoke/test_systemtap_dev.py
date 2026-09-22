import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file, check_static_lib


@allure.suite('systemtap-dev tests')
@pytest.mark.smoke
@pytest.mark.systemtap_dev
class TestSystemtapDev:
    '''systemtap-dev smoke test class'''

    @allure.title('systemtap-dev: check headers')
    @pytest.mark.minimal
    def test_systemtap_dev_headers(self, ssh_client: SshClient):
        '''Testing systemtap headers installed'''
        with allure.step('Check systemtap headers'):
            cmd = ssh_client.exec('test -e /usr/include/systemtap/stapmark.h', ignore_rc=True)
            assert cmd.rc == 0, f"systemtap-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('systemtap-dev: check shared libraries')
    @pytest.mark.minimal
    def test_systemtap_dev_shared_libraries(self, ssh_client: SshClient):
        '''Testing systemtap shared libraries installed'''
        with allure.step('Check staplog.so'):
            # Systemtap often provides specialized libs like staplog.so
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/systemtap/staplog.so')
            assert is_elf, f"systemtap-dev failed (shared library staplog.so check failed) out='{msg}', err=''"

    @allure.title('systemtap-dev: check static libraries')
    @pytest.mark.minimal
    def test_systemtap_dev_static_libraries(self, ssh_client: SshClient):
        '''Testing systemtap static libraries installed'''
        with allure.step('Check libasmsym.a'):
            is_static_lib, msg = check_static_lib(ssh_client, '/usr/lib/systemtap/libasmsym.a')
            assert is_static_lib, f"systemtap-dev failed (static library libasmsym.a check failed) out='{msg}', err=''"

    # pylint: disable=unused-argument
    @allure.title('systemtap-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_systemtap_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing systemtap basic workability via compilation with sdt markers'''
        ssh_client.put_file(f'{test_files_path}/test_systemtap_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'g++ -o {remote_tmp_path}/stap_dev_test {remote_tmp_path}/test_systemtap_dev.cpp &&\
{remote_tmp_path}/stap_dev_test', ignore_rc=True)
            assert cmd.rc == 0, f"systemtap-dev failed (compilation of sdt markers failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('systemtap-dev: check pkg-config')
    def test_systemtap_dev_pkgconfig(self, ssh_client: SshClient):
        '''Check if systemtap pkg-config file exists'''
        with allure.step('Check systemtap.pc'):
            cmd = ssh_client.exec('test -e /usr/share/pkgconfig/systemtap.pc', ignore_rc=True)
            assert cmd.rc == 0, f"systemtap-dev failed (pkg-config file not found) out='{cmd.stdout}', err='{cmd.stderr}'"
