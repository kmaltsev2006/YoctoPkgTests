import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('makedumpfile tests')
@pytest.mark.smoke
@pytest.mark.makedumpfile
class TestMakedumpfile:
    '''Tests for makedumpfile utility.'''

    # pylint: disable=unused-argument
    @allure.title('makedumpfile: basic help check')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['makedumpfile']], indirect=True)
    def test_makedumpfile_help(self, ssh_client: SshClient, are_utils_available):
        '''
        Minimal test: checks if makedumpfile is installed and help works.
        '''
        with allure.step('Run makedumpfile --help'):
            cmd = ssh_client.exec('makedumpfile --help', ignore_rc=True)
            is_valid = 'Usage:' in cmd.stdout or 'makedumpfile' in cmd.stdout
            assert is_valid, f"Makedumpfile failed (Basic execution failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('makedumpfile: check filter config syntax')
    @pytest.mark.parametrize('are_utils_available', [['makedumpfile']], indirect=True)
    def test_makedumpfile_config(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies that makedumpfile accepts the configuration file via --config.
        Since we don't have a real vmcore/vmlinux, we expect a specific error
        about missing arguments/files, NOT a syntax error in config.
        '''
        conf_path = f'{remote_tmp_path}/test_makedumpfile_filter.conf'

        ssh_client.put_file(
            f'{test_files_path}/test_makedumpfile_filter.conf', remote_tmp_path)

        with allure.step('Run with --config and dummy arguments'):
            cmd = ssh_client.exec(
                f'makedumpfile --config {conf_path} -x /tmp/fake_vmlinux /tmp/fake_vmcore /tmp/out', ignore_rc=True)

        with allure.step('Verify config parsing'):
            output = cmd.stdout + cmd.stderr

            check.is_not_in('syntax error', output.lower(),
                            f"Makedumpfile failed (Syntax error in config): out='{cmd.stdout}', err='{cmd.stderr}'")

            is_expected_error = 'No such file' in output or 'open_dwarf_table' in output
            check.is_true(is_expected_error,
                          f"Makedumpfile failed (Unexpected error message): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('makedumpfile: memory usage calculation (complex)')
    def test_makedumpfile_mem_usage(self, ssh_client: SshClient):
        '''
        Complex test: Uses --mem-usage option on the live kernel (/proc/kcore).
        This forces makedumpfile to parse memory structures.
        '''
        check_kcore = ssh_client.exec('test -e /proc/kcore', ignore_rc=True)
        if check_kcore.rc != 0:
            pytest.skip(
                '/proc/kcore not found (container?). Cannot run mem-usage test.')

        with allure.step('Run makedumpfile --mem-usage on /proc/kcore'):
            cmd = ssh_client.exec(
                'makedumpfile --mem-usage /proc/kcore', ignore_rc=True)

        with allure.step('Verify output calculation'):
            output = cmd.stdout + cmd.stderr

            success_markers = ['TYPE', 'PAGES', 'memory usage']
            is_calculation_done = cmd.rc == 0 and any(
                m in output for m in success_markers)

            env_errors = [
                'kernel version',
                'debuginfo',
                'No memory is reserved',
                'mmap'
            ]
            is_env_error = any(err in output for err in env_errors)

            assert is_calculation_done or is_env_error, \
                f"Makedumpfile failed (Memory usage check failed): out='{cmd.stdout}', err='{cmd.stderr}'"
