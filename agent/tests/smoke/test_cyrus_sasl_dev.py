import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cyrus-sasl-dev tests')
@pytest.mark.smoke
@pytest.mark.cyrus_sasl_dev
class TestCyrusSaslDev:
    '''cyrus-sasl-dev smoke tests'''

    @allure.title('cyrus-sasl-dev: header exists')
    @pytest.mark.minimal
    def test_header_exists(self, ssh_client: SshClient):
        '''Check that sasl header file exists'''
        with allure.step('Checking that /usr/include/sasl/sasl.h exists'):
            cmd = ssh_client.exec(
                'ls /usr/include/sasl/sasl.h', 
                ignore_rc=True
            )
            assert cmd.rc == 0, 'sasl.h header is missing — cyrus-sasl-dev not installed'

    @allure.title('cyrus-sasl-dev: compile minimal program')
    def test_compile_minimal_sasl(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Compile simple program linking with sasl'''
        with allure.step('Creating minimal C program for sasl'):
            ssh_client.exec(
                'echo "#include <sasl/sasl.h>\nint main(){ return 0; }"'
                f'> {remote_tmp_path}/test_sasl.c'
            )

        with allure.step('Compiling minimal program with -lsasl2'):
            cmd = ssh_client.exec(f'gcc {remote_tmp_path}/test_sasl.c -o {remote_tmp_path}/test_sasl -lsasl2', ignore_rc=True)
            assert cmd.rc == 0, f'Compilation failed: {cmd.stderr}'
