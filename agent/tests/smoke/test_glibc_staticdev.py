import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib

@allure.suite('glibc-staticdev tests')
@pytest.mark.smoke
@pytest.mark.glibc_staticdev
class TestGlibcStaticDev:
    '''glibc-staticdev smoke tests'''

    @allure.title('glibc-staticdev: static libc exists')
    @pytest.mark.minimal
    def test_glibc_staticdev_libc_exists(self, ssh_client: SshClient):
        cmd = ssh_client.exec(
            'ls /usr/lib*/libc.a 2>/dev/null | head -n1', ignore_rc=True)
        libpath = cmd.stdout.strip()
        assert cmd.rc == 0 and libpath, 'Static libc not found'

    @allure.title('glibc-staticdev: static libc is valid archive')
    @pytest.mark.minimal
    def test_glibc_staticdev_file(self, ssh_client: SshClient):
        cmd = ssh_client.exec(
            'ls /usr/lib*/libc.a 2>/dev/null | head -n1', ignore_rc=True)
        libpath = cmd.stdout.strip()
        is_static, msg = check_static_lib(ssh_client, libpath)
        assert is_static, msg

    # pylint: disable=unused-argument
    @allure.title('glibc-staticdev: compile and run static program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_glibc_staticdev_compile_and_run_static_program(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        remote_source = f'{remote_tmp_path}/test_glibc_static.c'
        remote_bin = f'{remote_tmp_path}/test_glibc_static'

        ssh_client.exec(
            'echo "#include <stdio.h>\n'
            'int main(){ printf(\\"52\\"); return 0; }" > ' + remote_source
        )

        cmd = ssh_client.exec(
            f'gcc {remote_source} -o {remote_bin} -static && {remote_bin}',
            ignore_rc=True
        )

        assert cmd.rc == 0 and '52' in cmd.stdout, \
            f'Unexpected result: rc={cmd.rc}, out="{cmd.stdout}", err="{cmd.stderr}"'
