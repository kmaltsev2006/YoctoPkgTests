import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gperftools tests')
@pytest.mark.smoke
@pytest.mark.gperftools_dev
class TestGperftoolsDev:
    '''Tests for the gperftools (Google Performance Tools) development library'''

    @allure.title('gperftools-dev: minimal test')
    @pytest.mark.minimal
    def test_gperftools_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of gperftools (headers check)'''
        with allure.step('Check headers'):
            cmd = ssh_client.exec(
                'test -f /usr/include/gperftools/tcmalloc.h', ignore_rc=True)
            assert cmd.rc == 0, f"Gperftools failed (Header file 'tcmalloc.h' not found): out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('gperftools-dev: compile and link against libtcmalloc')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_tcmalloc_compile_and_run(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that we can compile a program linking against libtcmalloc
        and confirming the headers exist.
        '''
        source_path = f'{remote_tmp_path}/test_tcmalloc.cpp'
        binary_path = f'{remote_tmp_path}/test_tcmalloc_app'

        ssh_client.put_file(
            f'{test_files_path}/test_tcmalloc.cpp', remote_tmp_path)

        with allure.step('Compile with -ltcmalloc'):
            compile_cmd = f'g++ -o {binary_path} {source_path} -ltcmalloc'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Gperftools failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Run the compiled application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Gperftools failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}")

            check.is_in('tcmalloc allocation successful', cmd.stdout,
                        f"Gperftools failed (Allocation was not successful): out='{cmd.stdout}', err='{cmd.stderr}")
