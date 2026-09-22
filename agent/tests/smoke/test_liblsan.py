import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('liblsan tests')
@pytest.mark.smoke
@pytest.mark.liblsan
class TestLibLsanRuntime:
    '''Tests covering the main liblsan runtime package.'''

    @allure.title('liblsan: libraries test')
    @pytest.mark.minimal
    def test_liblsan_lib(self, ssh_client: SshClient):
        '''Test liblsan libraries installed'''
        with allure.step('Checking liblsan libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblsan.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('liblsan: detect memory leak (dynamic)')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_liblsan_dynamic_detection(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Compiles with -fsanitize=leak and expects the run to FAIL with specific exit code (23).
        """
        source_path = f'{remote_tmp_path}/test_liblsan.cpp'
        binary_path = f'{remote_tmp_path}/test_leak_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_liblsan.cpp', remote_tmp_path)

        with allure.step('Compile with -fsanitize=leak'):
            cmd = ssh_client.exec(f'g++ {source_path} -o {binary_path} -fsanitize=leak -g', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Liblsan failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run binary with LSAN enabled'):
            # LSAN_OPTIONS=exitcode=23 sets a custom exit code when a leak is detected
            cmd = ssh_client.exec(f'LSAN_OPTIONS=exitcode=23 {binary_path}', ignore_rc=True)

            check.equal(cmd.rc, 23, f"Liblsan failed (Leak not detected or wrong exit code): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('LeakSanitizer: detected memory leaks', cmd.stdout + cmd.stderr,
                        f"Liblsan failed (Sanitizer report missing): out='{cmd.stdout}', err='{cmd.stderr}'")
