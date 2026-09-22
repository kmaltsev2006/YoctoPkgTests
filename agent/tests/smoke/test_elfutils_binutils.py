import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('elfutils-binutils tests')
@pytest.mark.smoke
@pytest.mark.elfutils_binutils
class TestE2fsprogs:
    '''elfutils-binutils smoke test class'''

    @allure.title('elfutils-binutils: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'elfedit',
        'readelf',
    ])
    def test_elfutils_binutils_installation(self, ssh_client: SshClient, utility: str):
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'{utility} not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('elfedit: check workability')
    @pytest.mark.minimal
    def test_elfutils_binutils_elfedit_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check elfedit workability'):
            cmd = ssh_client.exec(
                f'elfedit {remote_tmp_path}/test_elfutils --output-mach k1om', ignore_rc=True)
            assert cmd.rc == 0, f'elfedit is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('readelf: check workability')
    @pytest.mark.minimal
    def test_elfutils_binutils_readelf_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check readelf workability'):
            cmd = ssh_client.exec(
                f'readelf {remote_tmp_path}/test_elfutils -h', ignore_rc=True)
            assert cmd.rc == 0 and all(c in cmd.stdout for c in [
                                       'Class', 'Machine', 'Flags']), f'readelf is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
