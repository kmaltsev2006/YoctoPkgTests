import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('icu-dev tests')
@pytest.mark.smoke
@pytest.mark.icu_dev
class TestIcuDev:
    '''icu-dev smoke test class'''

    @allure.title('icu-dev: development headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        'utypes.h',
        'ucnv.h',
        'ustring.h'
    ])
    def test_icu_headers(self, ssh_client: SshClient, header: str):
        '''Test that ICU header files are installed'''
        with allure.step('Checking some specific ICU headers'):
            cmd = ssh_client.exec(
                f'stat /usr/include/unicode/{header}', ignore_rc=True)
            assert cmd.rc == 0, f"icu-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('icu-dev: libraries test')
    @pytest.mark.minimal
    def test_icu_dev_lib(self, ssh_client: SshClient):
        '''Test icu-dev libraries installed'''
        with allure.step('Checking icu-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libicuuc.so')
            assert is_elf, f'icu-dev failed: {msg}'

    @allure.title('icu-dev: compile and run test')
    def test_icu_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test icu development headers and libraries'''
        ssh_client.put_file(
            f'{test_files_path}/test_icu_dev.cpp', remote_tmp_path)
        command = f'g++ {remote_tmp_path}/test_icu_dev.cpp -o {remote_tmp_path}/test_icu_dev -licuuc && {remote_tmp_path}/test_icu_dev'
        with allure.step('Compiling and running program using icu'):
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'ICU_DEV_SUCCESS' in cmd.stdout, f"icu-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"
