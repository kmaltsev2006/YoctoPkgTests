import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('lmdb-dev tests')
@pytest.mark.smoke
@pytest.mark.lmdb_dev
class TestLmdbDev:
    '''lmdb-dev smoke test class'''

    @allure.title('lmdb-dev: libraries test')
    @pytest.mark.minimal
    def test_lmdb_dev_lib(self, ssh_client: SshClient):
        with allure.step('Checking lmdb libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/liblmdb.so')
            check.is_true(is_elf, msg)

    @allure.title('lmdb-dev: headers test')
    @pytest.mark.minimal
    def test_lmdb_dev_headers(self, ssh_client: SshClient):
        with allure.step('Checking lmdb-dev headers'):
            cmd = ssh_client.exec('stat /usr/include/lmdb.h', ignore_rc=True)
            check.equal(cmd.rc, 0, f'lmdb headers not found: {cmd.stderr}')

    @allure.title('lmdb-dev: compilation and workability test')
    @pytest.mark.minimal
    @pytest.mark.require_packages(['gcc'])
    def test_lmdb_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        source_file = 'test_lmdb.c'
        binary_exec = f'{remote_tmp_path}/test_lmdb'

        with allure.step('Upload test source file'):
            ssh_client.put_file(f'{test_files_path}/{source_file}', remote_tmp_path)

        with allure.step('Compile and run'):
            command = f'gcc {remote_tmp_path}/{source_file} -o {binary_exec} -llmdb && {binary_exec}'
            cmd = ssh_client.exec(command, ignore_rc=True)

            check.equal(cmd.rc, 0, f'lmdb-dev compilation or execution failed: {cmd.stderr}')
            check.is_in('LMDB_TEST_PASS', cmd.stdout, f'Unexpected output: {cmd.stdout}')
