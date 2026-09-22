import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('krb5-dev tests')
@pytest.mark.smoke
@pytest.mark.krb5_dev
class TestKrb5Dev:
    '''krb5-dev smoke test class'''

    @allure.title('krb5-dev: headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/krb5.h',
        '/usr/include/gssapi.h',
        '/usr/include/com_err.h'
    ])
    def test_krb5_dev_headers(self, header, ssh_client: SshClient):
        '''Test krb5-dev headers installed'''
        with allure.step(f'Checking {header}'):
            cmd = ssh_client.exec(f'stat {header}', ignore_rc=True)
            assert cmd.rc == 0, f"krb5-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('krb5-dev: libraries test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', [
        '/usr/lib/libkrb5.so',
        '/usr/lib/libgssapi_krb5.so',
        '/usr/lib/libcom_err.so'
    ])
    def test_krb5_dev_libs(self, lib, ssh_client: SshClient):
        '''Test krb5-dev libraries installed'''
        with allure.step(f'Checking {lib}'):
            is_elf, msg = check_elf_file(ssh_client, lib)
            assert is_elf, f'krb5-dev failed: {msg}'

    @allure.title('krb5-dev: functional test')
    def test_krb5_dev_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with krb5 libraries'''
        ssh_client.put_file(
            f'{test_files_path}/krb5_test.c', remote_tmp_path)
        test_file = f'{remote_tmp_path}/krb5_test.c'
        test_binary = f'{remote_tmp_path}/krb5_test'

        with allure.step('Compiling and running test program'):
            cmd = ssh_client.exec(
                f'gcc {test_file} -o {test_binary} -lkrb5 -lgssapi_krb5 -lcom_err && {test_binary}',
                ignore_rc=True
            )
            assert cmd.rc == 0 and 'KRB5_FUNCTIONS_WORK' in cmd.stdout, f"krb5-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
