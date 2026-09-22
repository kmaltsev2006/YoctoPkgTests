import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libnl tests')
@pytest.mark.smoke
@pytest.mark.libnl
class TestLibNlRuntime:
    '''Tests covering the main libnl runtime package.'''

    @allure.title('libnl: libraries test')
    @pytest.mark.minimal
    def test_libnl_lib(self, ssh_client: SshClient):
        '''Test libnl libraries installed'''
        with allure.step('Checking libnl libraries'):
            # Проверяем наличие всех библиотек (обычно libnl-3.so.*)
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libnl-3.so*')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libnl: compile and run (core functionality)')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libnl_core_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Verifies nl_socket_alloc, nl_connect, and rtnl_link_alloc_cache.
        """
        source_path = f'{remote_tmp_path}/test_libnl.c'
        binary_path = f'{remote_tmp_path}/test_libnl_core_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_libnl.c', remote_tmp_path)

        with allure.step('Compile with libnl-3 and libnl-route-3'):
            compile_cmd = f'gcc {source_path} -o {binary_path} -I/usr/include/libnl3 -lnl-route-3 -lnl-3'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnl failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnl failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('LibNL Core: Socket created', cmd.stdout,
                        f"Libnl failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
