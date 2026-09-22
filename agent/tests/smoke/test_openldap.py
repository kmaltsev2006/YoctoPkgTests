import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('openldap tests')
@pytest.mark.smoke
@pytest.mark.openldap
class TestOpenldap:
    '''openldap smoke test class'''

    @allure.title('openldap: headers presence')
    @pytest.mark.minimal
    def test_openldap_headers(self, ssh_client: SshClient):
        '''Test that OpenLDAP headers are installed'''
        with allure.step('Checking OpenLDAP headers presence'):
            cmd = ssh_client.exec(
                'ls /usr/include/ldap.h 2>/dev/null',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'OpenLDAP failed (headers): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('openldap: shared library presence')
    @pytest.mark.minimal
    def test_openldap_shared_library(self, ssh_client: SshClient):
        '''Test that OpenLDAP shared library is installed'''
        with allure.step('Checking OpenLDAP shared library'):
            is_shared, msg = check_elf_file(
                ssh_client,
                '/usr/lib/libldap.so'
            )
            assert is_shared, f'OpenLDAP failed (shared library): {msg}'
