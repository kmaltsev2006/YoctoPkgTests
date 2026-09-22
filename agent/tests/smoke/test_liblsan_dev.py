import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('liblsan-dev tests')
@pytest.mark.smoke
@pytest.mark.liblsan_dev
class TestLibLsanDev:
    '''Tests covering liblsan-dev package.'''

    @allure.title('liblsan-dev: libraries test')
    @pytest.mark.minimal
    def test_liblsan_dev_lib(self, ssh_client: SshClient):
        '''Test liblsan-dev libraries installed'''
        with allure.step('Checking liblsan-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblsan.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('liblsan-dev: compile check')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_liblsan_dev_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Main test: Verifies that we can compile a program linking against liblsan.
        """
        source_path = f'{remote_tmp_path}/test_leak.cpp'
        binary_path = f'{remote_tmp_path}/test_leak_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_leak.cpp', remote_tmp_path)

        with allure.step('Compile with -fsanitize=leak'):
            cmd = ssh_client.exec(f'g++ {source_path} -o {binary_path} -fsanitize=leak', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Liblsan failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")
