import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('liburcu-dev tests')
@pytest.mark.smoke
@pytest.mark.liburcu_dev
class TestLiburcuDev:
    '''liburcu-dev smoke test class'''

    @allure.title('liburcu-dev: headers presence')
    @pytest.mark.minimal
    def test_liburcu_dev_headers(self, ssh_client: SshClient):
        '''Check that liburcu development headers are installed'''
        with allure.step('Checking liburcu header presence'):
            cmd = ssh_client.exec(
                'test -f /usr/include/urcu.h',
                ignore_rc=True
            )

        assert cmd.rc == 0, f'liburcu-dev failed (header not found): out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('liburcu-dev: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_liburcu_dev_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile and run program using liburcu headers'''
        remote_source = f'{remote_tmp_path}/test_liburcu.c'
        test_binary = f'{remote_tmp_path}/test_liburcu'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_liburcu.c',
                remote_source
            )

        with allure.step('Compiling test program with liburcu headers'):
            cmd = ssh_client.exec(
                f'gcc -o {test_binary} {remote_source} -lurcu',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'liburcu-dev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"'

        with allure.step('Running liburcu test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            assert cmd.rc == 0, f'liburcu-dev failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"'
