import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libidn2-dev tests')
@pytest.mark.smoke
@pytest.mark.libidn2_dev
class TestLibIdn2Dev:
    '''Tests for the libidn2-dev package.'''

    @allure.title('libidn2-dev: libraries test')
    @pytest.mark.minimal
    def test_libidn2_dev_lib(self, ssh_client: SshClient):
        '''Test libidn2-dev libraries installed'''
        with allure.step('Checking libidn2-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libidn2.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libidn2-dev: compile and run IDNA conversion')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libidn2_compilation_and_run(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that a C program linking against libidn2 compiles and runs correctly.
        Checks IDNA2008 encoding functionality (UTF-8 to ASCII/Punycode).
        '''
        source_path = f'{remote_tmp_path}/test_libidn2.c'
        binary_path = f'{remote_tmp_path}/test_idn2_app'

        ssh_client.put_file(
            f'{test_files_path}/test_libidn2.c', remote_tmp_path)

        with allure.step('Compile the C program linking libidn2'):
            cmd = ssh_client.exec(f'gcc {source_path} -o {binary_path} -lidn2', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libidn2 failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libidn2 failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            expected_punycode = 'xn--mnchen-3ya.de'
            check.is_in(expected_punycode, cmd.stdout,
                        f"Libidn2 failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
