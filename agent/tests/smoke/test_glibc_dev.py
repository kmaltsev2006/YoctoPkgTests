import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('glibc-dev tests')
@pytest.mark.smoke
@pytest.mark.glibc_dev
class TestGlibcDev:
    '''glibc-dev smoke tests'''

    @allure.title('glibc-dev: standard headers exist')
    @pytest.mark.minimal
    def test_glibc_dev_headers_exist(self, ssh_client: SshClient):
        '''Check that standard glibc headers exist'''
        with allure.step('Checking /usr/include/stdio.h and /usr/include/stdlib.h'):
            cmd = ssh_client.exec('ls /usr/include/stdio.h /usr/include/stdlib.h', ignore_rc=True)
            assert cmd.rc == 0, f'glibc-dev headers missing: out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('glibc-dev: compile minimal program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_glibc_dev_compile_minimal_program(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile and run a minimal program using standard glibc headers'''
        remote_source = f'{remote_tmp_path}/test_glibc_dev.c'
        remote_bin = f'{remote_tmp_path}/test_glibc_dev'

        with allure.step(f'Creating minimal C program at {remote_source}'):
            ssh_client.exec(
                'echo "#include <stdio.h>\n#include <stdlib.h>\n'
                'int main(){ char* s = getenv(\\"PATH\\"); return s ? 0 : 1; }" > '
                + remote_source
            )

        with allure.step(f'Compiling {remote_source} and running {remote_bin}'):
            cmd = ssh_client.exec(f'gcc {remote_source} -o {remote_bin} && {remote_bin}', ignore_rc=True)
            assert cmd.rc == 0, f'Program compilation or execution failed: {cmd.stderr}'
