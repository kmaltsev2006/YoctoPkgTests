import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient

@allure.suite('glibc-utils tests')
@pytest.mark.smoke
@pytest.mark.glibc_utils
class TestGlibcUtils:
    '''glibc-utils smoke tests'''

    @allure.title('glibc-utils: ldd binary exists')
    @pytest.mark.minimal
    def test_glibc_utils_ldd_exists(self, ssh_client: SshClient):
        '''Check that ldd utility exists'''
        with allure.step('Checking for ldd binary'):
            cmd = ssh_client.exec('which ldd', ignore_rc=True)
            assert cmd.rc == 0 and cmd.stdout.strip(), 'ldd utility not found — glibc-utils not installed'

    # pylint: disable=unused-argument
    @allure.title('glibc-utils: ldd functional check')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_glibc_utils_ldd_functional(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile a minimal C program and verify ldd reports libc'''
        remote_source = f'{remote_tmp_path}/test_ldd.c'
        remote_bin = f'{remote_tmp_path}/test_ldd'

        with allure.step('Creating minimal C program'):
            ssh_client.exec(f'echo "int main(){{return 0;}}" > {remote_source}')

        with allure.step('Compiling program'):
            cmd = ssh_client.exec(f'gcc {remote_source} -o {remote_bin}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'Compilation failed: {cmd.stderr}')

        with allure.step('Running ldd to check linked libraries'):
            cmd = ssh_client.exec(f'ldd {remote_bin}', ignore_rc=True)
            assert cmd.rc == 0 and 'libc.so' in cmd.stdout, f'ldd failed or libc not linked: out="{cmd.stdout}", err="{cmd.stderr}"'
