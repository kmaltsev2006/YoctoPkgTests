import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib

@allure.suite('gflags-staticdev tests')
@pytest.mark.smoke
@pytest.mark.gflags_staticdev
class TestGflagsStaticDev:
    '''gflags-staticdev smoke tests'''

    @allure.title('gflags-staticdev: static library exists')
    @pytest.mark.minimal
    def test_static_library_exists(self, ssh_client: SshClient):
        '''Check that libgflags.a exists'''
        with allure.step('Looking for libgflags.a in standard library paths'):
            cmd = ssh_client.exec('ls /usr/lib*/libgflags.a 2>/dev/null | head -n1', ignore_rc=True)
            libpath = cmd.stdout.strip()
            assert cmd.rc == 0 and libpath, f"Static libgflags (libgflags.a) not found: out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('gflags-staticdev: static library is valid')
    @pytest.mark.minimal
    def test_static_library_valid(self, ssh_client: SshClient):
        '''Check that libgflags.a is a valid static library'''
        cmd = ssh_client.exec('ls /usr/lib*/libgflags.a 2>/dev/null | head -n1', ignore_rc=True)
        libpath = cmd.stdout.strip()
        if cmd.rc != 0 or not libpath:
            pytest.skip('libgflags.a not found — skipping static library check')

        with allure.step(f'Checking if {libpath} is a valid static library'):
            is_static_lib, msg = check_static_lib(ssh_client, libpath)
            assert is_static_lib, msg

    # pylint: disable=unused-argument
    @allure.title('gflags-staticdev: compile minimal static-linked program')
    @pytest.mark.parametrize('are_utils_available', [['c++']], indirect=True)
    def test_compile_static_gflags(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile and run a small gflags program statically (-static) to verify static dev package'''
        with allure.step('Checking if C++ compiler is available'):
            cmd = ssh_client.exec('command -v c++', ignore_rc=True)
            if cmd.rc != 0:
                pytest.skip('C++ compiler not available — skipping gflags-staticdev test')

        remote_src = f'{remote_tmp_path}/test_gflags_static.cpp'
        remote_bin = f'{remote_tmp_path}/test_gflags_static'

        with allure.step('Uploading C++ static test program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_gflags_static.cpp',
                remote_src
            )

        with allure.step('Compiling and running program statically with -static -lgflags'):
            cmd = ssh_client.exec(
                f'c++ {remote_src} -std=c++11 -o {remote_bin} -static -lgflags && {remote_bin}', ignore_rc=True
            )
            assert cmd.rc == 0, f'Static program failed (static gflags not available?): {cmd.stderr}'
