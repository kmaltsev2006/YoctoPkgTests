import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('systemd-dev tests')
@pytest.mark.smoke
@pytest.mark.systemd_dev
class TestSystemdDev:
    '''systemd-dev smoke test class'''

    @allure.title('systemd-dev: check headers')
    @pytest.mark.minimal
    def test_systemd_dev_headers(self, ssh_client: SshClient):
        '''Testing systemd headers installed'''
        with allure.step('Check systemd headers'):
            cmd = ssh_client.exec('test -e /usr/include/systemd', ignore_rc=True)
            assert cmd.rc == 0, f"systemd-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('systemd-dev: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libsystemd.so', 'libudev.so'])
    def test_systemd_dev_shared_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing systemd shared libraries installed'''
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f"systemd-dev failed (shared library {lib} check failed) out='{msg}', err=''"

    # pylint: disable=unused-argument
    @allure.title('systemd-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_systemd_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing systemd basic workability via compilation'''
        ssh_client.put_file(f'{test_files_path}/test_systemd_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(
                f'g++ -o {remote_tmp_path}/sysd_test {remote_tmp_path}/test_systemd_dev.cpp -lsystemd && {remote_tmp_path}/sysd_test',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"systemd-dev failed (compilation or execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"
