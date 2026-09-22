import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('numactl-dev tests')
@pytest.mark.smoke
@pytest.mark.numactl_dev
class TestNumactlDev:
    '''numactl-dev smoke test class'''

    @allure.title('numactl-dev: headers presence')
    @pytest.mark.minimal
    def test_numactl_dev_headers(self, ssh_client: SshClient):
        '''Test that numactl development headers are installed'''
        with allure.step('Checking numa.h presence'):
            cmd = ssh_client.exec(
                'ls /usr/include/numa.h 2>/dev/null',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'numactl-dev failed (header): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('numactl-dev: shared library presence')
    @pytest.mark.minimal
    def test_numactl_dev_shared_library(self, ssh_client: SshClient):
        '''Test that libnuma shared library is installed'''
        with allure.step('Checking libnuma shared library ELF'):
            is_elf, msg = check_elf_file(
                ssh_client,
                '/usr/lib/libnuma.so'
            )
            assert is_elf, f'numactl-dev failed (shared library): {msg}'

    # pylint: disable=unused-argument
    @allure.title('numactl-dev: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_numactl_dev_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile and run test program using libnuma'''
        remote_source = f'{remote_tmp_path}/test_numactl.c'
        test_binary = f'{remote_tmp_path}/test_numactl'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_numactl.c',
                remote_source
            )

        with allure.step('Compiling test program with libnuma'):
            cmd = ssh_client.exec(
                f'gcc {remote_source} -o {test_binary} -lnuma -L/usr/lib -Wl,-rpath=/usr/lib',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'numactl-dev failed (compile): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running compiled test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(cmd.rc, 0, f'numactl-dev failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_in(
                'NUMA_OK',
                cmd.stdout,
                f'numactl-dev failed (output): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
