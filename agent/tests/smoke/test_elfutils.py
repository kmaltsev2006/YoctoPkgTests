import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('elfutils tests')
@pytest.mark.smoke
@pytest.mark.elfutils
class TestE2fsprogs:
    '''elfutils smoke test class'''

    @allure.title('elfutils: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'eu-stack',
        'eu-nm',
        'eu-size',
        'eu-strip',
        'eu-readelf',
        'eu-elflint',
        'eu-elfcompress',
    ])
    def test_elfutils_installation(self, ssh_client: SshClient, utility: str):
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'{utility} not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('eu-stack: check workability')
    @pytest.mark.minimal
    def test_elfutils_eu_stack_workability(self, ssh_client: SshClient):
        with allure.step('Check eu-stack workability'):
            cmd = ssh_client.exec_sudo('eu-stack -p 1', ignore_rc=True)
            assert cmd.rc == 0 or 'PID 1 - process' in cmd.stdout, f'eu-stack is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('eu-nm: check workability')
    @pytest.mark.minimal
    def test_elfutils_eu_nm_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check eu-nm workability'):
            cmd = ssh_client.exec(
                f'eu-nm {remote_tmp_path}/test_elfutils', ignore_rc=True)
            assert cmd.rc == 0 and all(c in cmd.stdout for c in [
                                       'Name', 'Size', 'Section']), f'eu-nm is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('eu-size: check workability')
    @pytest.mark.minimal
    def test_elfutils_eu_size_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check eu-size workability'):
            cmd = ssh_client.exec(
                f'eu-size {remote_tmp_path}/test_elfutils', ignore_rc=True)
            assert cmd.rc == 0 and all(c in cmd.stdout for c in [
                                       'text', 'data', 'bss']), f'eu-size is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('eu-strip: check workability')
    @pytest.mark.minimal
    def test_elfutils_eu_strip_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check eu-strip workability'):
            cmd = ssh_client.exec(
                f'eu-strip {remote_tmp_path}/test_elfutils', ignore_rc=True)
            assert cmd.rc == 0, f'eu-strip failed: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('eu-readelf: check workability')
    @pytest.mark.minimal
    def test_elfutils_eu_readelf_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check eu-readelf workability'):
            cmd = ssh_client.exec(
                f'eu-readelf -S {remote_tmp_path}/test_elfutils', ignore_rc=True)
            assert cmd.rc == 0 and all(c in cmd.stdout for c in [
                                       '.text', '.data', '.bss']), f'eu-readelf is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('eu-elflint: check workability')
    @pytest.mark.minimal
    def test_elfutils_eu_elflint_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check eu-elflint workability'):
            cmd = ssh_client.exec(
                f'eu-elflint {remote_tmp_path}/test_elfutils', ignore_rc=True)
            assert cmd.rc == 0 and cmd.stdout == 'No errors', f'eu-elflint is broken: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('eu-elfcompress: check workability')
    @pytest.mark.minimal
    def test_elfutils_eu_elfcompress_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        with allure.step('Copy elf to target'):
            ssh_client.put_file(f'{test_files_path}/test_elfutils', remote_tmp_path)

        with allure.step('Check eu-elfcompress workability'):
            cmd = ssh_client.exec(
                f'eu-elfcompress {remote_tmp_path}/test_elfutils --verbose', ignore_rc=True)
            assert cmd.rc == 0 and f'processing: {remote_tmp_path}/test_elfutils' in cmd.stdout,\
                f'eu-elfcompress is broken: out="{cmd.stdout}", err="{cmd.stderr}"'
