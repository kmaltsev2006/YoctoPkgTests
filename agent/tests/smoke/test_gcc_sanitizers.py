import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gcc-sanitizers tests')
@pytest.mark.smoke
@pytest.mark.gcc_sanitizers
class TestGccSanitizers:
    '''gcc-sanitizers smoke tests'''

    # pylint: disable=unused-argument
    @allure.title('gcc-sanitizers: ASan detects memory error')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_asan_detects_error(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile ASan C program with memory error and verify sanitizer catches it'''

        remote_source = f'{remote_tmp_path}/test_asan_error.c'
        remote_executable = f'{remote_tmp_path}/test_asan_error'

        with allure.step(f'Copying test_asan_error.c to target at {remote_source}'):
            ssh_client.put_file(f'{test_files_path}/test_asan_error.c', remote_source)

        with allure.step('Compiling with AddressSanitizer'):
            cmd = ssh_client.exec(f'gcc {remote_source} -o {remote_executable} -fsanitize=address', ignore_rc=True)
            check.equal(cmd.rc, 0, f'ASan compilation failed: {cmd.stderr}')

        with allure.step('Running ASan executable'):
            cmd = ssh_client.exec(remote_executable, ignore_rc=True)
            check.is_true(cmd.rc != 0, 'ASan did not detect the memory error')
            check.is_in('ERROR', cmd.stderr, 'ASan error message not found in stderr')

    # pylint: disable=unused-argument
    @allure.title('gcc-sanitizers: UBSan detects undefined behavior')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_ubsan_detects_error(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile UBSan C program with undefined behavior and verify sanitizer catches it'''

        remote_source = f'{remote_tmp_path}/test_ubsan_error.c'
        remote_executable = f'{remote_tmp_path}/test_ubsan_error'

        with allure.step(f'Copying test_ubsan_error.c to target at {remote_source}'):
            ssh_client.put_file(f'{test_files_path}/test_ubsan_error.c', remote_source)

        with allure.step('Compiling with UndefinedBehaviorSanitizer'):
            cmd = ssh_client.exec(f'gcc {remote_source} -o {remote_executable} -fsanitize=undefined', ignore_rc=True)
            check.equal(cmd.rc, 0, f'UBSan compilation failed: {cmd.stderr}')

        with allure.step('Running UBSan executable'):
            cmd = ssh_client.exec(remote_executable, ignore_rc=True)
            check.is_true(cmd.rc != 0, 'UBSan did not detect undefined behavior')
            check.is_in('runtime error', cmd.stderr.lower(), 'UBSan error message not found in stderr')
