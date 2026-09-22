import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('gpgme-dev tests')
@pytest.mark.smoke
@pytest.mark.gpgme_dev
class TestGpgmeDev:
    '''Tests for the GPGME (GnuPG Made Easy) development library'''

    @allure.title('gpgme-dev: libraries test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libgpgme.so',
                                 'libgpgmepp.so'
                             ])
    def test_gpgme_dev_lib(self, lib: str, ssh_client: SshClient):
        '''Test gpgme-dev libraries installed'''
        with allure.step('Checking gpgme-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f'gpgme-dev failed: {msg}'

    @allure.title('gpgme-dev: minimal test')
    @pytest.mark.minimal
    def test_gpgme_dev_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of gpgme-dev'''
        with allure.step('Check pkg-config for gpgme'):
            cmd = ssh_client.exec(
                'pkg-config --modversion gpgme', ignore_rc=True)
            assert cmd.rc == 0, f"GPGME failed (GPGME development files not found via pkg-config): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('gpgme-dev: compile and init library context')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_gpgme_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that we can compile a program linking against libgpgme
        using flags provided by gpgme-config.
        '''
        source_path = f'{remote_tmp_path}/test_gpgme.c'
        binary_path = f'{remote_tmp_path}/test_gpgme_app'

        ssh_client.put_file(f'{test_files_path}/test_gpgme.c', remote_tmp_path)

        with allure.step('Compile using flag -lgpgme'):
            compile_cmd = f'gcc -o {binary_path} {source_path} -lgpgme'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"GPGME failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"GPGME failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('GPGME Context created successfully', cmd.stdout,
                        f"GPGME failed (Context was not created): out='{cmd.stdout}', err='{cmd.stderr}'")
