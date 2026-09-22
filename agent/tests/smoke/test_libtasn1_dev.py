import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libtasn1 tests')
@pytest.mark.smoke
@pytest.mark.libtasn1
class TestLibTasn1Dev:
    '''Tests for libtasn1-dev package.'''

    @allure.title('libtasn1-dev: libraries test')
    @pytest.mark.minimal
    def test_libtasn1_dev_lib(self, ssh_client: SshClient):
        '''Test libtasn1-dev libraries installed'''
        with allure.step('Checking libtasn1-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libtasn1.so')
            assert is_elf, msg

    @allure.title('libtasn1-dev: headers test')
    @pytest.mark.minimal
    def test_libtasn1_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/libtasn1.h', ignore_rc=True)
            assert cmd.rc == 0, f"Libtasn1-dev failed (Header file 'libtasn1.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('libtasn1-dev: compile and run version check')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libtasn1_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies that a C program linking against libtasn1 compiles and runs correctly.
        Checks output of asn1_check_version(NULL).
        '''
        source_path = f'{remote_tmp_path}/test_libtasn1.c'
        binary_path = f'{remote_tmp_path}/test_libtasn1_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_libtasn1.c', remote_tmp_path)

        with allure.step('Compile dynamically with -ltasn1'):
            cmd = ssh_client.exec(
                f'gcc {source_path} -o {binary_path} -ltasn1', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libtasn1 failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libtasn1 failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('libtasn1 initialized successfully', cmd.stdout,
                        f"Libtasn1 failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
