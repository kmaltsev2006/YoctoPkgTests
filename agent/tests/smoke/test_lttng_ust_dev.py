import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('lttng-ust-dev tests')
@pytest.mark.smoke
@pytest.mark.lttng_ust_dev
class TestLttngUstDev:
    '''lttng-ust-dev smoke test class'''

    @allure.title('lttng-ust-dev: libraries test')
    @pytest.mark.minimal
    def test_lttng_ust_dev_lib(self, ssh_client: SshClient):
        with allure.step('Checking lttng-ust library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblttng-ust.so')
            check.is_true(is_elf, msg)

    @allure.title('lttng-ust-dev: headers test')
    @pytest.mark.minimal
    def test_lttng_ust_dev_headers(self, ssh_client: SshClient):
        with allure.step('Checking lttng-ust-dev headers'):
            cmd = ssh_client.exec('test -f /usr/include/lttng/ust-version.h', ignore_rc=True)
            check.equal(cmd.rc, 0, f'lttng-ust headers not found: {cmd.stderr}')

    @allure.title('lttng-ust-dev: compilation and workability test')
    @pytest.mark.minimal
    @pytest.mark.require_packages(['gcc'])
    def test_lttng_ust_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        source_file = 'test_lttng_ust.c'
        binary_exec = f'{remote_tmp_path}/test_lttng_ust'

        with allure.step('Upload test source file'):
            ssh_client.put_file(f'{test_files_path}/{source_file}', remote_tmp_path)

        with allure.step('Compile and run'):
            # lttng-ust usually requires dl library as well
            command = f'gcc {remote_tmp_path}/{source_file} -o {binary_exec} -llttng-ust -ldl && {binary_exec}'
            cmd = ssh_client.exec(command, ignore_rc=True)

            check.equal(cmd.rc, 0, f'lttng-ust-dev compilation failed: {cmd.stderr}')
            check.is_in('LTTNG_UST_VERSION_OK', cmd.stdout, f'Unexpected output: {cmd.stdout}')
