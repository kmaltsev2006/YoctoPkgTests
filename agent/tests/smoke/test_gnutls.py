import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('gnutls-dev tests')
@pytest.mark.smoke
@pytest.mark.gnutls_dev
class TestGnutlsDev:
    '''Tests for the GnuTLS development library'''

    @allure.title('gnutls-dev: libraries test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libgnutls.so'
                             ])
    def test_gnutls_dev_lib(self, lib: str, ssh_client: SshClient):
        '''Test gnutls-dev libraries installed'''
        with allure.step('Checking gnutls-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f'gnutls-dev failed: {msg}'

    # pylint: disable=unused-argument
    @allure.title('gnutls-dev: compile and run library initialization')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_gnutls_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that we can compile a program linking against libgnutls
        using flags -I/usr/include/p11-kit-1 -lgnutls
        '''
        source_path = f'{remote_tmp_path}/test_gnutls.c'
        binary_path = f'{remote_tmp_path}/test_gnutls_app'

        ssh_client.put_file(
            f'{test_files_path}/test_gnutls.c', remote_tmp_path)

        with allure.step('Compile using flag -lgnutls'):
            compile_cmd = f'gcc -o {binary_path} {source_path} -I/usr/include/p11-kit-1 -lgnutls'

            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"GnuTLS failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Run the compiled application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"GnuTLS failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}")
            check.is_in('GnuTLS initialized successfully',
                        cmd.stdout, f"GnuTLS failed (Unexpected output): out='{cmd.stdout}', err='{cmd.stderr}")
