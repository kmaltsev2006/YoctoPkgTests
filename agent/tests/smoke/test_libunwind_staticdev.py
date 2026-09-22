import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libunwind-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libunwind_staticdev
class TestLibunwindStaticdev:
    '''libunwind-staticdev smoke test class'''

    @allure.title('libunwind-staticdev: static libraries presence')
    @pytest.mark.minimal
    def test_libunwind_static_libraries(self, ssh_client: SshClient):
        '''Check that libunwind static libraries are installed'''
        with allure.step('Searching for libunwind static libraries'):
            cmd = ssh_client.exec(
                "find /usr/lib /usr/lib64 /lib -name 'libunwind*.a' 2>/dev/null",
                ignore_rc=True
            )
            libs = [path for path in cmd.stdout.splitlines() if path.strip()]
            assert libs, f'libunwind failed (static library check): out="{cmd.stdout}", err="{cmd.stderr}"'

        with allure.step('Verifying that found libraries are static'):
            for lib in libs:
                is_static, msg = check_static_lib(ssh_client, lib)
                check.is_true(is_static, f'libunwind failed (static library validation for {lib}): {msg}')

    @allure.title('libunwind-staticdev: headers presence')
    @pytest.mark.minimal
    def test_libunwind_staticdev_headers(self, ssh_client: SshClient):
        '''Check that libunwind headers are installed'''
        with allure.step('Checking libunwind headers'):
            cmd = ssh_client.exec(
                'ls /usr/include/libunwind.h 2>/dev/null',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'libunwind failed (headers check): out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('libunwind-staticdev: compile test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libunwind_staticdev_compile(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        '''Compile test program using libunwind headers'''
        remote_source = f'{remote_tmp_path}/test_libunwind.c'
        object_file = f'{remote_tmp_path}/test_libunwind.o'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(
                f'{test_files_path}/test_libunwind.c',
                remote_source
            )

        with allure.step('Compiling test source into object file'):
            cmd = ssh_client.exec(
                f'gcc -c {remote_source} -o {object_file}',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'libunwind failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"')
