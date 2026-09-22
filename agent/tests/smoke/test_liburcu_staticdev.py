import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('liburcu-staticdev tests')
@pytest.mark.smoke
@pytest.mark.liburcu_staticdev
class TestLiburcuStaticdev:
    '''liburcu-staticdev smoke test class'''
    @allure.title('liburcu-staticdev: static library presence')
    @pytest.mark.minimal
    def test_liburcu_staticdev_library(self, ssh_client: SshClient):
        '''Check that liburcu static library is installed'''
        with allure.step('Searching for liburcu static library'):
            cmd = ssh_client.exec(
                'find /usr/lib /usr/lib64 /lib -name "liburcu*.a" 2>/dev/null | head -n 1',
                ignore_rc=True
            )
            assert cmd.stdout.strip(), f'liburcu-staticdev failed (static library not found): out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('liburcu-staticdev: compile and run static test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_liburcu_staticdev_compile(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        remote_source = f'{remote_tmp_path}/test_liburcu.c'
        test_binary = f'{remote_tmp_path}/test_liburcu_static'

        ssh_client.put_file(
            f'{test_files_path}/test_liburcu.c',
            remote_source
        )

        with allure.step('Compiling test program with static liburcu'):
            cmd = ssh_client.exec(
                f'gcc -static {remote_source} -o {test_binary} -lurcu',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'liburcu-staticdev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running statically compiled program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(cmd.rc, 0, f'liburcu-staticdev failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"')
