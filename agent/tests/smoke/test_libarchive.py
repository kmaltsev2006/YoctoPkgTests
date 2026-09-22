import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file
import pytest_check as check


@allure.suite('libarchive tests')
@pytest.mark.smoke
@pytest.mark.libarchive
class TestLibarchive:
    '''libarchive smoke test class'''

    @allure.title('libarchive: library exists')
    @pytest.mark.minimal
    def test_libarchive_lib(self, ssh_client: SshClient):
        '''Test libarchive library installed'''
        with allure.step('Checking libarchive library'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libarchive.so')
            assert is_elf, f'libarchive failed: {msg}'

    @allure.title('libarchive: bsdtar version test')
    @pytest.mark.minimal
    def test_bsdtar_version(self, ssh_client: SshClient):
        '''Test bsdtar version'''
        with allure.step('Checking bsdtar version'):
            cmd = ssh_client.exec('bsdtar --version', ignore_rc=True)
            assert cmd.rc == 0 and 'bsdtar' in cmd.stdout.lower(), \
                f"bsdtar failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libarchive: bsdtar basic operations test')
    @pytest.mark.minimal
    def test_bsdtar_basic_operations(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test bsdtar create and extract operations'''
        test_file_name = 'test_file.txt'
        test_file = f'{remote_tmp_path}/{test_file_name}'
        test_archive = f'{remote_tmp_path}/test_archive.tar'

        # Create test file
        ssh_client.exec(f"echo 'Test content for archive' > {test_file}")

        # Create tar archive
        with allure.step('Create tar archive with bsdtar'):
            cmd = ssh_client.exec(
                f'bsdtar -cf {test_archive} -C {remote_tmp_path} {test_file_name} ', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"bsdtar failed: out='{cmd.stdout}', err='{cmd.stderr}'")

        # Remove original file
        ssh_client.exec(f'rm {test_file}')

        # Extract tar archive
        with allure.step('Extract tar archive with bsdtar'):
            cmd = ssh_client.exec(
                f'bsdtar -xf {test_archive} -C {remote_tmp_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"bsdtar failed: out='{cmd.stdout}', err='{cmd.stderr}'")

        # Verify extracted file
        with allure.step('Verify extracted file content'):
            cmd = ssh_client.exec(f'cat {test_file}', ignore_rc=True)
            check.is_in('Test content for archive', cmd.stdout,
                        f"bsdtar failed (invalid content): out='{cmd.stdout}', err='{cmd.stderr}'")
