import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('lvm2-dev tests')
@pytest.mark.smoke
@pytest.mark.lvm2_dev
class TestLvm2Dev:
    '''lvm2-dev smoke test class'''

    @allure.title('lvm2-dev: libraries test')
    @pytest.mark.minimal
    def test_lvm2_dev_lib(self, ssh_client: SshClient):
        with allure.step('Checking devmapper library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libdevmapper.so')
            check.is_true(is_elf, msg)

    @allure.title('lvm2-dev: headers test')
    @pytest.mark.minimal
    def test_lvm2_dev_headers(self, ssh_client: SshClient):
        with allure.step('Checking lvm2/devmapper headers'):
            cmd = ssh_client.exec('stat /usr/include/libdevmapper.h', ignore_rc=True)
            check.equal(cmd.rc, 0, f'devmapper headers not found: {cmd.stderr}')

    @allure.title('lvm2-dev: compilation and workability test')
    @pytest.mark.minimal
    @pytest.mark.require_packages(['gcc'])
    def test_lvm2_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        source_file = 'test_lvm2.c'
        binary_exec = f'{remote_tmp_path}/test_lvm2'

        with allure.step('Upload test source file'):
            ssh_client.put_file(f'{test_files_path}/{source_file}', remote_tmp_path)

        with allure.step('Compile and run'):
            command = f'gcc {remote_tmp_path}/{source_file} -o {binary_exec} -ldevmapper && {binary_exec}'
            cmd = ssh_client.exec(command, ignore_rc=True)

            check.equal(cmd.rc, 0, f'lvm2-dev compilation failed: {cmd.stderr}')
            check.is_in('DEVMAPPER_VERSION_OK', cmd.stdout, f'Unexpected output: {cmd.stdout}')
