import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libxslt tests')
@pytest.mark.smoke
@pytest.mark.libxslt
class TestLibxslt:
    '''libxslt smoke test class'''

    @allure.title('libxslt: libraries test')
    @pytest.mark.minimal
    def test_libxslt_lib(self, ssh_client: SshClient):
        with allure.step('Checking libxslt libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libxslt.so')
            check.is_true(is_elf, msg)

    @allure.title('libxslt: compilation and workability test')
    @pytest.mark.minimal
    @pytest.mark.require_packages(['gcc'])
    def test_libxslt_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        source_file = 'test_libxslt.c'
        binary_exec = f'{remote_tmp_path}/test_libxslt'

        with allure.step('Upload test source file'):
            ssh_client.put_file(f'{test_files_path}/{source_file}', remote_tmp_path)

        with allure.step('Compile and run'):
            # libxslt requires headers from libxml2 and linking with both lxslt and lxml2
            command = (
                f'gcc {remote_tmp_path}/{source_file} -o {binary_exec} '
                f'-I/usr/include/libxml2 -lxslt -lxml2 && {binary_exec}'
            )
            cmd = ssh_client.exec(command, ignore_rc=True)

            check.equal(cmd.rc, 0, f'libxslt compilation or execution failed: {cmd.stderr}')
            check.is_in('LIBXSLT_INITIALIZED', cmd.stdout, f'Unexpected output: {cmd.stdout}')
