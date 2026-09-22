import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('lttng-tools-dev tests')
@pytest.mark.smoke
@pytest.mark.lttng_tools_dev
class TestLttngToolsDev:
    '''lttng-tools-dev smoke test class'''

    @allure.title('lttng-tools-dev: libraries test')
    @pytest.mark.minimal
    def test_lttng_tools_dev_lib(self, ssh_client: SshClient):
        '''Testing lttng-ctl library installed'''
        with allure.step('Checking lttng-ctl library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblttng-ctl.so')
            check.is_true(is_elf, msg)

    @allure.title('lttng-tools-dev: headers test')
    @pytest.mark.minimal
    def test_lttng_tools_dev_headers(self, ssh_client: SshClient):
        '''Testing lttng-tools-dev headers installed'''
        with allure.step('Checking lttng-tools-dev headers'):
            cmd = ssh_client.exec('stat /usr/include/lttng/lttng.h', ignore_rc=True)
            check.equal(cmd.rc, 0, f'lttng-tools headers not found: {cmd.stderr}')

    # pylint: disable=unused-argument
    @allure.title('lttng-tools-dev: check workability')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_lttng_tools_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing lttng-tools-dev API workability'''

        ssh_client.put_file(
            f'{test_files_path}/test_lttng_tools.c', remote_tmp_path)

        with allure.step('Compile and run'):
            # Compile with liblttng-ctl
            cmd = ssh_client.exec(
                f'gcc -o {remote_tmp_path}/test_lttng_tools {remote_tmp_path}/test_lttng_tools.c '
                f'-llttng-ctl && {remote_tmp_path}/test_lttng_tools',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'lttng-tools-dev compilation or execution failed: {cmd.stderr}')
            check.is_in('LTTNG_API_FUNCTIONAL', cmd.stdout, f'Unexpected output: {cmd.stdout}')
