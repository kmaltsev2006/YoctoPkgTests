import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('util-linux-libuuid tests')
@pytest.mark.smoke
@pytest.mark.util_linux_libuuid
class TestUtilLinuxLibuuid:
    '''util-linux-libuuid smoke test class'''

    @allure.title('util-linux-libuuid: check shared library')
    @pytest.mark.minimal
    def test_util_linux_libuuid_shared_library(self, ssh_client: SshClient):
        '''Testing libuuid shared library installed'''
        with allure.step('Check libuuid.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libuuid.so.1')
            assert is_elf, f"util-linux-libuuid failed (libuuid.so.1 check failed) out='{msg}', err=''"

    @allure.title('util-linux-libuuid: check uuidgen utility')
    @pytest.mark.minimal
    def test_util_linux_libuuid_uuidgen_installation(self, ssh_client: SshClient):
        '''Check installed uuidgen via which'''
        with allure.step('Check uuidgen installation'):
            cmd = ssh_client.exec('which uuidgen', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-libuuid failed (uuidgen not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('uuidgen: check workability')
    def test_util_linux_libuuid_uuidgen_workability(self, ssh_client: SshClient):
        '''Test uuidgen basic functionality'''
        with allure.step('Generate random UUID'):
            cmd = ssh_client.exec('uuidgen -r', ignore_rc=True)
            check.equal(cmd.rc, 0, f"util-linux-libuuid failed (uuidgen execution error) out='{cmd.stdout}', err='{cmd.stderr}'")

            uuid_output = cmd.stdout.strip()
            check.equal(len(uuid_output), 36, f"util-linux-libuuid failed (invalid UUID format) out='{uuid_output}', err=''")

    @allure.title('uuidgen: check time-based generation')
    def test_util_linux_libuuid_uuidgen_time(self, ssh_client: SshClient):
        '''Test uuidgen time-based functionality'''
        with allure.step('Generate time-based UUID'):
            cmd = ssh_client.exec('uuidgen -t', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-libuuid failed (uuidgen -t failed) out='{cmd.stdout}', err='{cmd.stderr}'"
