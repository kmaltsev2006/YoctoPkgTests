import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cmake tests')
@pytest.mark.smoke
@pytest.mark.cmake
class TestCMake:
    '''CMake smoke test class'''

    @allure.title('cmake: minimal test')
    @pytest.mark.minimal
    def test_cmake_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of CMake'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('cmake --version', ignore_rc=True)
            check.equal(cmd.rc, 0,
                        f"CMake failed (CMake is not installed): out='{cmd.stdout}', err='{cmd.stderr}'")
        with allure.step('Simple check on echo'):
            cmd_echo = ssh_client.exec(
                "cmake -E echo 'CMake is alive'", ignore_rc=True)
            check.is_in('CMake is alive', cmd_echo.stdout,
                        f"CMake failed (CMake is not responding): out='{cmd.stdout}', err='{cmd.stderr}'")

    # pylint: disable=unused-argument
    @allure.title('cmake: full cycle (configure, build, run)')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_cmake_full_cycle(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Tests the full lifecycle of a CMake project'''
        files = ['main.cpp', 'CMakeLists.txt']
        for file in files:
            ssh_client.put_file(
                f'{test_files_path}/test_cmake/{file}', remote_tmp_path)
        ssh_client.create_remote_dir(f'{remote_tmp_path}/build')
        with allure.step('Running CMake full cycle'):
            command_configure = f'cd {remote_tmp_path}/build && cmake {remote_tmp_path} && cmake --build . && ./my_app'
            cmd = ssh_client.exec(command_configure, ignore_rc=True)
            assert cmd.rc == 0, f"CMake failed: out='{cmd.stdout}', err='{cmd.stderr}"
