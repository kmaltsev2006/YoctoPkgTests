import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libnl-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libnl_staticdev
class TestLibNlStaticDev:
    '''Tests covering libnl-staticdev package.'''

    @allure.title('libnl-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libnl-3.a',
                                 'libnl-route-3.a'
                             ])
    def test_libnl_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing libnl static libraries'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg

    @allure.title('libnl-staticdev: minimal test')
    @pytest.mark.minimal
    def test_libnl_static_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of libnl-static (static library check)'''
        with allure.step('Check for static library file via GCC'):
            cmd = ssh_client.exec(
                'gcc -print-file-name=libnl-3.a', ignore_rc=True)
            assert cmd.rc == 0 and '/' in cmd.stdout, \
                f"Libnl Static failed (Static library libnl-3.a not found in GCC search path): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('libnl-staticdev: static linkage check')
    @pytest.mark.parametrize('are_utils_available', [['gcc', 'ldd']], indirect=True)
    def test_libnl_static_link(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Verifies static linking against libnl-3.
        """
        source_path = f'{remote_tmp_path}/test_libnl_static.c'
        binary_path = f'{remote_tmp_path}/test_libnl_core_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_libnl_static.c', remote_tmp_path)

        with allure.step('Compile statically'):
            compile_cmd = f'gcc {source_path} -o {binary_path} -static -I/usr/include/libnl3 -lnl-route-3 -lnl-3 -lpthread'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnl Static failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnl Static failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('LibNL Core: Socket created', cmd.stdout,
                        f"Libnl Static failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify binary does not use shared library'):
            # Check that it's not dynamically linked against libnl
            cmd = ssh_client.exec(
                f'! ldd {binary_path} | grep libnl-3', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Libnl Static failed (Binary is dynamically linked against libnl, expected static): out='{cmd.stdout}', err='{cmd.stderr}'")
