import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cmake-dev tests')
@pytest.mark.smoke
@pytest.mark.cmake_dev
class TestCmakeDev:
    '''cmake-dev smoke tests'''

    @allure.title('cmake-dev: check standard modules')
    @pytest.mark.minimal
    def test_cmake_modules(self, ssh_client: SshClient):
        '''Check that standard CMake modules are installed'''
        with allure.step('Checking that FindThreads module exists in CMake Modules directory'):
            cmd = ssh_client.exec('ls /usr/share/cmake*/Modules/FindThreads.cmake', ignore_rc=True)
            assert cmd.rc == 0, 'FindThreads.cmake missing — cmake-dev might be not installed or incomplete'

    # pylint: disable=unused-argument
    @allure.title('cmake-dev: configure minimal project')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_cmake_configure_project(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Test minimal CMake project can be configured'''
        with allure.step('Writing CMakeLists.txt and test_cmake.c for a minimal project'):
            ssh_client.exec(
                'echo "cmake_minimum_required(VERSION 3.10)\n'
                'project(TestCmake)\n'
                'add_executable(test_app test_cmake.c)" '
                f'> {remote_tmp_path}/CMakeLists.txt'
            )
            ssh_client.exec(
                "echo 'int main(){ return 0; }'" f' > {remote_tmp_path}/test_cmake.c'
            )

        with allure.step('Running cmake to configure the minimal project'):
            cmd = ssh_client.exec(f'cd {remote_tmp_path} && cmake .', ignore_rc=True)
            assert cmd.rc == 0, f'cmake configuration failed: {cmd.stderr}'
