import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('liblzma tests')
@pytest.mark.smoke
@pytest.mark.liblzma
class TestLibLzma:
    """Tests for the liblzma compression library."""

    @allure.title('liblzma: libraries test')
    @pytest.mark.minimal
    def test_liblzma_lib(self, ssh_client: SshClient):
        '''Test liblzma libraries installed'''
        with allure.step('Checking liblzma libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblzma.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('liblzma: compile and run simple version check')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_liblzma_usage(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None) -> None:
        """
        Verifies that we can compile a program linking against liblzma
        and that it returns the library version string.
        """
        source_path = f'{remote_tmp_path}/test_liblzma.c'
        binary_path = f'{remote_tmp_path}/test_lzma_app'

        ssh_client.put_file(
            f'{test_files_path}/test_liblzma.c', remote_tmp_path)

        with allure.step('Compile application with -llzma'):
            cmd = ssh_client.exec(
                f'gcc -o {binary_path} {source_path} -llzma', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Liblzma failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run compiled application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Liblzma failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('LZMA Library Version', cmd.stdout,
                        f"Liblzma failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
