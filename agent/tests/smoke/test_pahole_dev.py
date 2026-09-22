import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('pahole-dev tests')
@pytest.mark.smoke
@pytest.mark.pahole_dev
class TestPaholeDev:
    '''pahole-dev smoke test class'''

    @allure.title('pahole-dev: headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        'dwarves.h',
        'dwarves_emit.h',
    ])
    def test_pahole_dev_headers(self, header: str, ssh_client: SshClient):
        '''Test pahole-dev installed headers'''
        with allure.step('Checking pahole-dev headers'):
            cmd = ssh_client.exec(
                f'stat /usr/include/dwarves/{header}', ignore_rc=True)
            assert cmd.rc == 0, f"pahole-dev failed (header {header} not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('pahole-dev: libraries test')
    @pytest.mark.minimal
    def test_pahole_dev_lib(self, ssh_client: SshClient):
        '''Test pahole-dev libraries installed'''
        with allure.step('Checking pahole-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libdwarves.so')
            assert is_elf, f'pahole-dev failed: {msg}'

    @allure.title('pahole-dev: functionality test')
    def test_pahole_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test pahole-dev library functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_pahole_dev.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/test_pahole_dev.c'
        test_binary = f'{remote_tmp_path}/pahole_dev_test'

        with allure.step('Compiling with libdwarves'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -ldwarves',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"pahole-dev failed (compile error): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Running test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pahole-dev test failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('CUS_INIT_SUCCESS', cmd.stdout,
                        f"pahole-dev test failed: out='{cmd.stdout}', err='{cmd.stderr}'")
