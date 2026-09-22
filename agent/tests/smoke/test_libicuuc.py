import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libicuuc tests')
@pytest.mark.smoke
@pytest.mark.libicuuc
class TestLibIcuUc:
    '''Tests for the libicuuc library (ICU Common).'''

    @allure.title('libicuuc-dev: libraries test')
    @pytest.mark.minimal
    def test_libicuuc_dev_lib(self, ssh_client: SshClient):
        '''Test libicuuc-dev libraries installed'''
        with allure.step('Checking libicuuc-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libicuuc.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libicuuc: compile and run version check')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libicu_compilation_and_run(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None) -> None:
        '''
        Verifies that a C program linking against libicuuc compiles and runs correctly.
        '''
        source_path = f'{remote_tmp_path}/test_libicuuc.c'
        binary_path = f'{remote_tmp_path}/test_icu_app'

        ssh_client.put_file(
            f'{test_files_path}/test_libicuuc.c', remote_tmp_path)

        with allure.step('Compile the C program linking libicuuc'):
            cmd = ssh_client.exec(f'gcc {source_path} -o {binary_path} -licuuc', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libicuuc failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libicuuc failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('ICU Version:', cmd.stdout,
                        f"Libicuuc failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
