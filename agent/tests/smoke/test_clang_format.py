import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('clang-format tests')
@pytest.mark.smoke
@pytest.mark.clang_format
class TestClangFormat:
    '''clang-format smoke test class'''
    @allure.title('clang-format: version check')
    @pytest.mark.minimal
    def test_clang_format_version(self, ssh_client: SshClient):
        '''Checking clang-format installed version'''
        with allure.step('Checking clang-format version'):
            cmd = ssh_client.exec('clang-format --version', ignore_rc=True)
            assert cmd.rc == 0, f"clang-format failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('clang-format: basic formatting test')
    @pytest.mark.minimal
    def test_clang_format(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test clang-format basic functionality'''
        test_file_name = 'test_clang_format.cpp'
        with allure.step('Preparing test file'):
            ssh_client.put_file(
                f'{test_files_path}/{test_file_name}', remote_tmp_path)
            file_size = int(ssh_client.exec(
                f'wc -m < {remote_tmp_path}/{test_file_name}').stdout)
        with allure.step('Testing output formatting'):
            command = f"cat {remote_tmp_path}/{test_file_name} | clang-format"
            cmd = ssh_client.exec(command, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"clang-format failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            # Formatting should add whitespaces and other syms
            check.is_true(len(cmd.stdout) > file_size,
                          f"clang-format failed (expected formatted code ({len(cmd.stdout)}) to be longer ({file_size})):\
                              out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_true('main()' in cmd.stdout,
                          f"clang-format failed (invalid formatted code): out='{cmd.stdout}', err='{cmd.stderr}'")
