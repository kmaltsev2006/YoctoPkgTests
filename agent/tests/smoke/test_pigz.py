import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('pigz tests')
@pytest.mark.smoke
@pytest.mark.pigz
class TestPigz:
    '''pigz smoke test class'''

    @allure.title('pigz: version test')
    @pytest.mark.minimal
    def test_pigz_version(self, ssh_client: SshClient):
        '''Test pigz version command'''
        with allure.step('Checking pigz version'):
            cmd = ssh_client.exec('pigz --version', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pigz failed (version check): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('pigz', cmd.stdout.lower(),
                        f"pigz version doesn't contain 'pigz': out='{cmd.stdout}', err='{cmd.stderr}'")

    def basic_pigz_compression_cycle(self, ssh_client: SshClient, remote_tmp_path: str, pigz_flags: str = '') -> None:
        '''Performs basic pigz compression and decompression with given flags'''
        test_file = f'{remote_tmp_path}/test_pigz.txt'
        compressed_file = f'{test_file}.gz'

        with allure.step('Creating test file'):
            test_content = 'This is a test file for pigz compression'
            ssh_client.exec(f"echo '{test_content}' > {test_file}")

        with allure.step('Compressing with pigz'):
            cmd = ssh_client.exec(
                f'pigz {pigz_flags} {test_file} 2>&1', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pigz compression failed: out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Checking compressed file exists'):
            cmd = ssh_client.exec(f'stat {compressed_file}', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pigz compressed file not created: out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Decompressing with pigz'):
            cmd = ssh_client.exec(
                f'pigz -d -k {compressed_file} 2>&1', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pigz decompression failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            cmd = ssh_client.exec(f'stat {test_file}', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pigz decompressed file not found: out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verifying decompressed content'):
            cmd = ssh_client.exec(f'cat {test_file}', ignore_rc=True)
            check.equal(cmd.stdout, test_content,
                        f"pigz decompressed file differs from original: out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('pigz: basic compression test')
    def test_pigz_basic_compression(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test basic pigz compression and decompression'''
        self.basic_pigz_compression_cycle(ssh_client, remote_tmp_path)

    @allure.title('pigz: parallel compression test')
    def test_pigz_parallel_compression(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test pigz parallel compression with -p option'''
        self.basic_pigz_compression_cycle(
            ssh_client, remote_tmp_path, '-p 2')
