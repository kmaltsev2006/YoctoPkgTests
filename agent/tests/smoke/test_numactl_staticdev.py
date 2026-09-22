import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('numactl-staticdev tests')
@pytest.mark.smoke
@pytest.mark.numactl_staticdev
class TestNumactlStaticdev:
    '''numactl-staticdev smoke test class'''

    @allure.title('numactl-staticdev: headers presence')
    @pytest.mark.minimal
    def test_numactl_staticdev_headers(self, ssh_client: SshClient):
        '''Test that numactl development headers are installed'''
        with allure.step('Checking numa.h presence'):
            cmd = ssh_client.exec(
                'ls /usr/include/numa.h 2>/dev/null',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'numactl-staticdev failed (header): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('numactl-staticdev: static library presence')
    @pytest.mark.minimal
    def test_numactl_staticdev_library(self, ssh_client: SshClient):
        '''Test that libnuma static library is installed'''
        with allure.step('Checking libnuma static library format'):
            is_static, msg = check_static_lib(
                ssh_client,
                '/usr/lib/libnuma.a'
            )
            assert is_static, f'numactl-staticdev failed (static library): {msg}'

    # pylint: disable=unused-argument
    @allure.title('numactl-staticdev: compile and run static test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_numactl_staticdev_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile and run test program using static libnuma'''
        remote_source = f'{remote_tmp_path}/test_numactl.c'
        test_binary = f'{remote_tmp_path}/test_numactl_static'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_numactl.c',
                remote_source
            )

        with allure.step('Compiling test program with static libnuma'):
            cmd = ssh_client.exec(
                f'gcc -static {remote_source} -lnuma -o {test_binary}',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'numactl-staticdev failed (compile): err="{cmd.stderr}"')

        with allure.step('Running compiled test program'):
            cmd = ssh_client.exec(
                test_binary,
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'numactl-staticdev failed (run): err="{cmd.stderr}"')
            check.is_in(
                'NUMA_OK',
                cmd.stdout,
                f'numactl-staticdev failed (output): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
