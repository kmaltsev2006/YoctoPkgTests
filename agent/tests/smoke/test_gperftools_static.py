import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('gperftools-static tests')
@pytest.mark.smoke
@pytest.mark.gperftools_staticdev
class TestGperftoolsStaticDev:
    '''Tests for the gperftools-staticdev (Google Performance Tools) development library'''

    @allure.title('gperftools-staticdev: headers test')
    @pytest.mark.minimal
    def test_gperftools_static_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Cheaking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/gperftools/tcmalloc.h', ignore_rc=True)
            assert cmd.rc == 0, f"Gperftools Static failed (Header file 'tcmalloc.h' not found): out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=duplicate-code
    @allure.title('gperftools-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libtcmalloc.a',
                                 'libtcmalloc_debug.a',
                                 'libtcmalloc_minimal.a',
                                 'libtcmalloc_minimal_debug.a'
                             ])
    def test_gperftools_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing gperftools static libraries'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg

    @allure.title('gperftools-staticdev: minimal test')
    @pytest.mark.minimal
    def test_gperftools_static_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of gperftools-static (static library check)'''
        with allure.step('Check for static library file via GCC'):
            cmd = ssh_client.exec(
                'g++ -print-file-name=libtcmalloc.a', ignore_rc=True)
            assert cmd.rc == 0, \
                f"Gperftools Static failed (Static library libtcmalloc.a not found in GCC search path): out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('gperftools-staticdev: compile and link against libtcmalloc')
    @pytest.mark.parametrize('are_utils_available', [['g++', 'ldd']], indirect=True)
    def test_tcmalloc_compile_and_run(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that we can compile a program linking against libtcmalloc
        and confirming the headers exist.
        '''

        source_path = f'{remote_tmp_path}/test_tcmalloc.cpp'
        binary_path = f'{remote_tmp_path}/test_tcmalloc_app'

        ssh_client.put_file(f'{test_files_path}/test_tcmalloc.cpp', remote_tmp_path)

        with allure.step('Compile with -static -ltcmalloc -lunwind -Wl,--allow-multiple-definition'):
            compile_cmd = f'g++ -static -o {binary_path} {source_path} -ltcmalloc -lunwind -Wl,--allow-multiple-definition'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Gperftools Static failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Run the compiled application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Gperftools Static failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}")
            check.is_in('tcmalloc allocation successful', cmd.stdout,
                        f"Gperftools Static failed (Allocation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Verify binary does not use shared library'):
            cmd = ssh_client.exec(
                f'! ldd {binary_path} | grep libtcmalloc', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Gperftools Static failed (Binary is dynamically, expected static): out='{cmd.stdout}', err='{cmd.stderr}")
