import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libnsl2-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libnsl2_staticdev
class TestLibNsl2StaticDev:
    '''Tests covering libnsl2-staticdev package.'''

    @allure.title('libnsl2-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libnsl.a'
                             ])
    def test_libnsl2_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing libnsl2 static libraries'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg

    @allure.title('libnsl2-staticdev: minimal test')
    @pytest.mark.minimal
    def test_libnsl2_static_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of libnsl2-static (static library check)'''
        with allure.step('Check for static library file via GCC'):
            cmd = ssh_client.exec('gcc -print-file-name=libnsl.a', ignore_rc=True)
            assert cmd.rc == 0 and '/' in cmd.stdout, \
                f"Libnsl2 Static failed (Static library libnsl.a not found in GCC search path): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('libnsl2-staticdev: compile and run (static linkage)')
    @pytest.mark.parametrize('are_utils_available', [['gcc', 'pkg-config', 'ldd']], indirect=True)
    def test_libnsl2_staticdev_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Main test: Verifies static compilation against libnsl.
        """
        source_path = f'{remote_tmp_path}/test_libnsl_static.c'
        binary_path = f'{remote_tmp_path}/test_nsl_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_libnsl_static.c', remote_tmp_path)

        with allure.step('Compile statically'):
            compile_cmd = f'gcc {source_path} -o {binary_path} -static -I/usr/include/tirpc -lnsl -ltirpc -lpthread'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnsl2 Static failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the static binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libnsl2 Static failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('NSL function executed', cmd.stdout,
                        f"Libnsl2 Static failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify binary does not use shared library'):
            cmd = ssh_client.exec(
                f'! ldd {binary_path} | grep libnsl', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Libnsl2 Static failed (Binary is dynamically linked against libnsl, expected static): out='{cmd.stdout}', err='{cmd.stderr}'")
