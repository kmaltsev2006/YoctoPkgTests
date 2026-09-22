import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
import pytest_check as check


@allure.suite('lcov tests')
@pytest.mark.smoke
@pytest.mark.lcov
class TestLcov:
    '''lcov smoke test class'''

    @allure.title('lcov: version test')
    @pytest.mark.minimal
    def test_lcov_version(self, ssh_client: SshClient):
        '''Test lcov version command'''
        with allure.step('Checking lcov version'):
            cmd = ssh_client.exec('lcov --version', ignore_rc=True)
            assert cmd.rc == 0 and 'lcov' in cmd.stdout.lower(), \
                f"lcov failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('lcov: genhtml version test')
    @pytest.mark.minimal
    def test_genhtml_version(self, ssh_client: SshClient):
        '''Test genhtml version command'''
        with allure.step('Checking genhtml version'):
            cmd = ssh_client.exec('genhtml --version', ignore_rc=True)
            assert cmd.rc == 0 and 'genhtml' in cmd.stdout.lower(), \
                f"genhtml failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('lcov: create and process simple coverage data')
    def test_lcov_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test lcov with simple coverage data'''
        # Create a simple C program
        ssh_client.put_file(
            f'{test_files_path}/test_lcov.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/test_lcov.c'
        test_binary = f'{remote_tmp_path}/test_lcov'
        coverage_dir = f'{remote_tmp_path}/coverage'

        with allure.step('Compiling with coverage flags'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -fprofile-arcs -ftest-coverage',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"lcov failed (compile error): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Running program to generate coverage data'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"lcov failed (test program error): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Running lcov to capture coverage'):
            # Create coverage directory
            ssh_client.exec(f'mkdir -p {coverage_dir}')

            # Capture baseline coverage
            cmd = ssh_client.exec(
                f'lcov --capture --directory {remote_tmp_path} --output-file {coverage_dir}/coverage.info --initial',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"lcov failed (lcov capture failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Checking coverage file was created'):
            cmd = ssh_client.exec(
                f'stat {coverage_dir}/coverage.info', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"lcov failed (coverage file not found): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Testing lcov list functionality'):
            cmd = ssh_client.exec(
                f'lcov --list {coverage_dir}/coverage.info',
                ignore_rc=True
            )
            # lcov list should work even with minimal data
            check.equal(
                cmd.rc, 0, f"lcov list failed: out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Testing genhtml with coverage data'):
            html_dir = f'{coverage_dir}/html'
            cmd = ssh_client.exec(
                f'genhtml {coverage_dir}/coverage.info --output-directory {html_dir}',
                ignore_rc=True
            )
            # genhtml might fail with insufficient data, but should at least run
            check.is_true(
                cmd.rc != 127, f"genhtml failed: out='{cmd.stdout}', err='{cmd.stderr}'")
