import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libnl-genl tests')
@pytest.mark.smoke
@pytest.mark.libnl_genl
class TestLibNlGenl:
    '''Tests covering libnl-genl package.'''

    @allure.title('libnl-genl: libraries test')
    @pytest.mark.minimal
    def test_libnl_genl_lib(self, ssh_client: SshClient):
        '''Test libnl-genl libraries installed'''
        with allure.step('Checking libnl-genl libraries'):
            # libnl-genl обычно идет как libnl-genl-3.so
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libnl-genl-3.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libnl-genl: generic netlink functionality')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libnl_genl_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Compiles and runs a C program using libnl-genl-3.
        """
        source_path = f'{remote_tmp_path}/test_libnl_genl.c'
        binary_path = f'{remote_tmp_path}/test_libnl_genl_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_libnl_genl.c', remote_tmp_path)

        with allure.step('Compile with libnl-genl-3'):
            compile_cmd = f'gcc {source_path} -o {binary_path} $(pkg-config --cflags --libs libnl-3.0 libnl-genl-3.0)'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnl-genl failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnl-genl failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('LibNL Genl: Connected', cmd.stdout,
                        f"Libnl-genl failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
