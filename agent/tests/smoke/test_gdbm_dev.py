import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gdbm-dev tests')
@pytest.mark.smoke
@pytest.mark.gdbm_dev
class TestGdbmDev:
    '''gdbm-dev smoke tests'''

    @allure.title('gdbm-dev: header exists')
    @pytest.mark.minimal
    def test_gdbm_dev_header_exists(self, ssh_client: SshClient):
        '''Check that gdbm header file exists'''
        with allure.step('Verifying /usr/include/gdbm.h header'):
            cmd = ssh_client.exec('ls /usr/include/gdbm.h', ignore_rc=True)
            assert cmd.rc == 0, 'gdbm.h header is missing — gdbm-dev not installed'

    # pylint: disable=unused-argument
    @allure.title('gdbm-dev: compile and run functional program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_gdbm_dev_compile_and_run_program(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile test_gdbm_dev.c and verify functionality'''
        local_source = f'{test_files_path}/test_gdbm_dev.c'
        remote_source = f'{remote_tmp_path}/test_gdbm_dev.c'
        remote_bin = f'{remote_tmp_path}/test_gdbm_dev'

        with allure.step(f'Copying test_gdbm_dev.c to target at {remote_source}'):
            ssh_client.put_file(local_source, remote_source)

        with allure.step(f'Compiling and running {remote_source} with -lgdbm && {remote_bin}'):
            cmd = ssh_client.exec(
                f'gcc {remote_source} -o {remote_bin} -lgdbm', ignore_rc=True
            )
            assert cmd.rc == 0, f'Program failed: {cmd.stderr}'
