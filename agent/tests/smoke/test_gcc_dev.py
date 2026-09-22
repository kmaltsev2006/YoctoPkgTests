import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gcc-dev tests')
@pytest.mark.smoke
@pytest.mark.gcc_dev
class TestGccDev:
    '''gcc-dev smoke tests'''

    @allure.title('gcc-dev: header exists')
    @pytest.mark.minimal
    def test_gcc_dev_header_exists(self, ssh_client: SshClient):
        '''Check that standard GCC headers exist'''
        with allure.step('Checking that stdio.h header exists'):
            cmd = ssh_client.exec('ls /usr/include/stdio.h', ignore_rc=True)
            assert cmd.rc == 0, 'stdio.h header is missing — gcc-dev not installed'

    # pylint: disable=unused-argument
    @allure.title('gcc-dev: compile and run functional program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_gcc_dev_compile_and_run_functional_program(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile gcc_dev.cpp and check functionality'''
        remote_source = f'{remote_tmp_path}/gcc_dev.cpp'
        remote_executable = f'{remote_tmp_path}/test_gcc'

        with allure.step('Copying C++ source to target'):
            ssh_client.put_file(f'{test_files_path}/test_gcc_dev.cpp', remote_source)

        with allure.step(f'Compiling {remote_source} with gcc and running'):
            cmd = ssh_client.exec(f'gcc {remote_source} -o {remote_executable} && {remote_executable}', ignore_rc=True)
            assert cmd.rc == 0, f'Program failed: {cmd.stderr}'
