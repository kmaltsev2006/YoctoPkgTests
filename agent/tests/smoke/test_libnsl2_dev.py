import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libnsl2-dev tests')
@pytest.mark.smoke
@pytest.mark.libnsl2_dev
class TestLibNsl2Dev:
    '''Tests covering libnsl2-dev package (headers, pkg-config, dynamic link).'''

    @allure.title('libnsl2-dev: libraries test')
    @pytest.mark.minimal
    def test_libnsl2_dev_lib(self, ssh_client: SshClient):
        '''Test libnsl2-dev libraries installed'''
        with allure.step('Checking libnsl2-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libnsl.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libnsl2-dev: compile and run (dynamic linkage)')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libnsl2_dev_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Main test: Verifies that we can compile and run a program linking against libnsl.
        """
        source_path = f'{remote_tmp_path}/test_libnsl.c'
        binary_path = f'{remote_tmp_path}/test_nsl_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_libnsl.c', remote_tmp_path)

        with allure.step('Compile dynamically'):
            compile_cmd = f'gcc {source_path} -o {binary_path} -I/usr/include/tirpc -lnsl -ltirpc'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnsl2 failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnsl2 failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('NSL function executed', cmd.stdout,
                        f"Libnsl2 failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
