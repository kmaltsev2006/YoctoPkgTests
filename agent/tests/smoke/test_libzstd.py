import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libzstd tests')
@pytest.mark.smoke
@pytest.mark.libzstd
class TestLibzstd:
    '''libzstd smoke test class'''

    @allure.title('libzstd: libraries test')
    @pytest.mark.minimal
    def test_libzstd_lib(self, ssh_client: SshClient):
        with allure.step('Checking libzstd libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libzstd.so')
            check.is_true(is_elf, msg)

    @allure.title('libzstd: compilation and workability test')
    @pytest.mark.minimal
    @pytest.mark.require_packages(['gcc'])
    def test_libzstd_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        source_file = 'test_libzstd_check.c'
        binary_exec = f'{remote_tmp_path}/test_libzstd'

        with allure.step('Upload test source file'):
            ssh_client.put_file(f'{test_files_path}/{source_file}', remote_tmp_path)

        with allure.step('Compile and run'):
            command = f'gcc {remote_tmp_path}/{source_file} -o {binary_exec} -lzstd && {binary_exec}'
            cmd = ssh_client.exec(command, ignore_rc=True)

            check.equal(cmd.rc, 0, f'libzstd compilation or execution failed: {cmd.stderr}')
            check.is_in('ZSTD_VERSION_OK', cmd.stdout, f'Unexpected output: {cmd.stdout}')
