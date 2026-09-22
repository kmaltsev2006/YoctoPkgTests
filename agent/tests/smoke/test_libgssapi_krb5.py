import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('libgssapi-krb5 tests')
@pytest.mark.smoke
@pytest.mark.libgssapi_krb5
class TestLibgssapiKrbs:
    '''libgssapi-krb5 smoke test class'''

    @allure.title('libgssapi-krb5: library test')
    def test_libgssapi_krb5_library(self, ssh_client: SshClient) -> None:
        '''Test libgssapi-krb5 library installed'''
        with allure.step('Check if libgssapi_krb5.so is a valid ELF file'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libgssapi_krb5.so')
            assert is_elf, msg
