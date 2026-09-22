import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('gflags-dev tests')
@pytest.mark.smoke
@pytest.mark.gflags_dev
class TestGflagsDev:
    '''gflags-dev smoke tests'''

    @allure.title('gflags-dev: header exists')
    @pytest.mark.minimal
    def test_header_exists(self, ssh_client: SshClient):
        '''Check that gflags header file exists'''
        with allure.step('Checking for gflags header in common include paths'):
            cmd = ssh_client.exec(
                'ls /usr/include/gflags/gflags.h /usr/include/gflags.h 2>/dev/null | head -n1',
                ignore_rc=True
            )
            assert cmd.rc == 0 and cmd.stdout.strip(), 'gflags header not found — gflags-dev not installed'

    # pylint: disable=unused-argument
    @allure.title('gflags-dev: compile and run sample program')
    @pytest.mark.parametrize('are_utils_available', [['c++']], indirect=True)
    def test_compile_and_run_gflags_program(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile a small C++ program that uses gflags and run it (checks linkage and runtime)'''
        remote_src = f'{remote_tmp_path}/test_gflags_dev.cpp'
        remote_bin = f'{remote_tmp_path}/test_gflags_dev'

        with allure.step('Uploading C++ sample program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_gflags_dev.cpp',
                remote_src
            )

        with allure.step('Compiling and running sample program with -lgflags'):
            cmd = ssh_client.exec(
                f'c++ {remote_src} -std=c++11 -o {remote_bin} -lgflags && {remote_bin}',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'Program failed: {cmd.stderr}'
