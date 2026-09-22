import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('openldap-dev tests')
@pytest.mark.smoke
@pytest.mark.openldap_dev
class TestOpenldapDev:
    '''openldap-dev smoke test class'''

    @allure.title('openldap-dev: headers presence')
    @pytest.mark.minimal
    def test_openldap_dev_headers(self, ssh_client: SshClient):
        '''Test that OpenLDAP development headers are installed'''
        with allure.step('Checking OpenLDAP headers presence'):
            cmd = ssh_client.exec(
                'ls /usr/include/ldap.h 2>/dev/null',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'OpenLDAP-dev failed (headers): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('openldap-dev: shared library presence')
    @pytest.mark.minimal
    def test_openldap_dev_shared_library(self, ssh_client: SshClient):
        '''Test that OpenLDAP shared library is installed'''
        with allure.step('Checking OpenLDAP shared library'):
            is_shared, msg = check_elf_file(
                ssh_client,
                '/usr/lib/libldap.so'
            )
            check.is_true(is_shared, f'OpenLDAP-dev failed (shared library): {msg}')

    # pylint: disable=unused-argument
    @allure.title('openldap-dev: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_openldap_dev_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile and run test program using OpenLDAP development files'''
        remote_source = f'{remote_tmp_path}/test_openldap.c'
        binary = f'{remote_tmp_path}/test_openldap'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_openldap.c',
                remote_source
            )

        with allure.step('Compiling and running OpenLDAP test program'):
            cmd = ssh_client.exec(
                f'gcc {remote_source} -o {binary} -lldap && {binary}',
                ignore_rc=True
            )

        check.equal(
            cmd.rc,
            0,
            f'OpenLDAP-dev failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"'
        )
        check.is_in(
            'LDAP_OK',
            cmd.stdout,
            f'OpenLDAP-dev failed (output): out="{cmd.stdout}", err="{cmd.stderr}"'
        )
