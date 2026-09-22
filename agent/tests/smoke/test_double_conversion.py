import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('double-conversion tests')
@pytest.mark.smoke
@pytest.mark.double_conversion
class TestDoubleConversion:
    '''Tests for the double-conversion development library'''

    @allure.title('double-conversion: minimal test')
    @pytest.mark.minimal
    def test_double_conversion_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of double-conversion (headers check)'''
        with allure.step('Check headers directory'):
            cmd = ssh_client.exec(
                'test -d /usr/include/double-conversion', ignore_rc=True)
            assert cmd.rc == 0, 'double-conversion headers not found in /usr/include/double-conversion'

    @allure.title('double-conversion: compile, link and run sample program')
    def test_double_conversion_works(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''
        Tests that we can compile a program linking against libdouble-conversion
        and that it correctly performs a double-to-string conversion.
        '''
        ssh_client.put_file(
            f'{test_files_path}/test_double_conv.cpp', remote_tmp_path)

        with allure.step('Compile and run against libdouble-conversion'):
            compile_cmd = f'g++ -o {remote_tmp_path}/test_double_conv_app {remote_tmp_path}/test_double_conv.cpp \
                -ldouble-conversion && {remote_tmp_path}/test_double_conv_app'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            assert cmd.rc == 0 and 'Converted: 3.14159' in cmd.stdout, \
                f"double_conversion failed: out='{cmd.stdout}', err='{cmd.stderr}"
