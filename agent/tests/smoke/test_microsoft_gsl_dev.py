import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('microsoft-gsl-dev tests')
@pytest.mark.smoke
@pytest.mark.microsoft_gsl_dev
class TestMicrosoftGslDev:
    '''Tests for microsoft-gsl-dev (Guidelines Support Library).'''

    @allure.title('microsoft-gsl-dev: headers test')
    @pytest.mark.minimal
    def test_microsoft_gsl_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            # Microsoft GSL is a header-only library
            cmd = ssh_client.exec(
                'test -f /usr/include/gsl/span', ignore_rc=True)
            assert cmd.rc == 0, f"Microsoft-gsl-dev failed (Header file 'gsl/span' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('microsoft-gsl-dev: compile and run')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_microsoft_gsl_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Main test: Verifies that a C++ program using gsl::span compiles and runs.
        '''
        source_path = f'{remote_tmp_path}/test_microsoft_gsl.cpp'
        binary_path = f'{remote_tmp_path}/test_gsl_app'

        ssh_client.put_file(
            f'{test_files_path}/test_microsoft_gsl.cpp', remote_tmp_path)

        with allure.step('Compile with g++ -std=c++14'):
            # GSL requires at least C++14
            cmd = ssh_client.exec(
                f'g++ -std=c++14 {source_path} -o {binary_path}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Microsoft-gsl-dev failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Microsoft-gsl-dev failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('GSL span initialized successfully', cmd.stdout,
                        f"Microsoft-gsl-dev failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")
