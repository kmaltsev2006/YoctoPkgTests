import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libxml2 tests')
@pytest.mark.smoke
@pytest.mark.libxml2
class TestLibxml2:
    '''libxml2 smoke test class'''

    @allure.title('libxml2: libraries test')
    @pytest.mark.minimal
    def test_libxml2_lib(self, ssh_client: SshClient):
        with allure.step('Checking libxml2 libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libxml2.so')
            check.is_true(is_elf, msg)

    @allure.title('libxml2: compilation and workability test')
    @pytest.mark.minimal
    @pytest.mark.require_packages(['gcc'])
    def test_libxml2_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        source_file = 'test_libxml2.c'
        binary_exec = f'{remote_tmp_path}/test_libxml2'

        with allure.step('Upload test source file'):
            ssh_client.put_file(f'{test_files_path}/{source_file}', remote_tmp_path)

        with allure.step('Compile and run'):
            # libxml2 requires special include path and linking
            command = (
                f'gcc {remote_tmp_path}/{source_file} -o {binary_exec} '
                f'-I/usr/include/libxml2 -lxml2 && {binary_exec}'
            )
            cmd = ssh_client.exec(command, ignore_rc=True)

            check.equal(cmd.rc, 0, f'libxml2 compilation or execution failed: {cmd.stderr}')
            check.is_in('PARSED', cmd.stdout, f'Unexpected output: {cmd.stdout}')
