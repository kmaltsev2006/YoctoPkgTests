import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('gflags tests')
@pytest.mark.smoke
@pytest.mark.gflags
class TestGflags:
    '''gflags smoke tests (runtime)'''

    @allure.title('gflags: shared library exists')
    @pytest.mark.minimal
    def test_gflags_shared_library_exists(self, ssh_client: SshClient):
        '''Check that libgflags shared library exists'''
        with allure.step('Looking for libgflags shared library in standard paths'):
            cmd = ssh_client.exec('ls /usr/lib*/libgflags.so* 2>/dev/null | head -n1', ignore_rc=True)
            libpath = cmd.stdout.strip()
            assert cmd.rc == 0 and libpath, f"gflags failed (shared library not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('gflags: shared library is valid ELF')
    @pytest.mark.minimal
    def test_gflags_shared_library_elf(self, ssh_client: SshClient):
        '''Check that libgflags is a valid ELF shared library'''
        cmd = ssh_client.exec('ls /usr/lib*/libgflags.so* 2>/dev/null | head -n1', ignore_rc=True)
        libpath = cmd.stdout.strip()
        if cmd.rc != 0 or not libpath:
            pytest.skip('libgflags not found — skipping ELF check')

        with allure.step(f'Checking if {libpath} is a valid ELF shared library'):
            is_elf, msg = check_elf_file(ssh_client, libpath)
            assert is_elf, f'gflags failed: {msg}'
